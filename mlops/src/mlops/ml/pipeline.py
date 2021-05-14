import json
from azureml.core import Dataset
from azureml.core import Datastore
from azureml.core import Environment
from azureml.core.compute import ComputeTarget
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import Pipeline
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from mlops.script.step import StepArgParser

class MlPipeline():

    def __init__(self, workspace):
        self.workspace = workspace

    def from_config(self, config):
        self.config = config

        steps = []
        for c in self.config.get("steps"):
            step = self.get_step(c)
            steps.append(step)

        pipeline = Pipeline(workspace=self.workspace, steps=steps)

        return pipeline

    def get_dataset(self, config):
        name = config.get("name")
        version = config.get("version")
        if version == "latest":
            version = None

        dataset = Dataset.get_by_name(
            workspace=self.workspace, 
            name=name, 
            version=version)
        
        return dataset

    def get_environment(self, config):
        name = config.get("name")
        pip_wheel_path = config.get("pip_wheel_path")
        requirements_path = config.get("requirements_path")

        environment = Environment.from_pip_requirements(name, requirements_path)

        whl_url = environment.add_private_pip_wheel(
            workspace=self.workspace, 
            file_path=pip_wheel_path, 
            exist_ok=True)
        environment.python.conda_dependencies.add_pip_package(whl_url)

        return environment

    def get_run_config(self, config):

        environment_config = config.get("environment")
        environment = self.get_environment(environment_config)

        cluster_name = config.get("cluster")
        cluster = ComputeTarget(workspace=self.workspace, name=cluster_name)

        pipeline_run_config = RunConfiguration()
        pipeline_run_config.target = cluster
        pipeline_run_config.environment = environment

        return pipeline_run_config

    def get_step_args(self, config, steps_config_key):
        arguments = []

        def args_to_dict(args):
            arg_flags = {}
            for k, v in args.items():
                arg_flags[k] = v["flag"]

            return arg_flags

            # return dict(map(lambda x: (x[0], x[1]["flag"]), StepArgParser.INPUT_ARGS.items()))

        if steps_config_key == "input":
            arg_flags =  args_to_dict(StepArgParser.INPUT_ARGS)

        elif steps_config_key == "output":
            arg_flags =  args_to_dict(StepArgParser.OUTPUT_ARGS)

        for c in config:
            io_type = c["type"]
            io_config = c["config"]
            io_config_str = json.dumps(io_config)

            try:
                arg_flag = arg_flags[io_type]

                if io_type == StepArgParser.ARG_TYPE_NAMED_INPUT:
                    arg_dataset = self.get_dataset(io_config)
                    named_input_key = io_config["as_named_input"]

                    dataset_argument = [arg_flag, arg_dataset.as_named_input(named_input_key)]

                    arg_flag_named_input_key = arg_flags[StepArgParser.ARG_TYPE_NAMED_INPUT_KEY]
                    named_input_key_argument = [arg_flag_named_input_key, named_input_key]

                    argument = dataset_argument + named_input_key_argument
                else:
                    argument = [arg_flag, io_config_str]

            except KeyError as e:
                raise ValueError(f"Invalid {steps_config_key} type: {io_type}")

            arguments.extend(argument)

        return arguments

    def get_pipeline_data(self, config):
        pipeline_data = []

        for c in config:            
            if c["type"] == StepArgParser.ARG_TYPE_PIPELINE_DATA:
                pconfig = c["config"]
                pname = pconfig["name"]
                pds = pconfig.get("datastore") or "default"

                if pds == "default":
                    use_ds = self.workspace.get_default_datastore()
                else:
                    use_ds = Datastore.get(workspace=self.workspace, datastore_name=pds)

                pd = PipelineData(pname, datastore=use_ds)

                pipeline_data.append(pd)        

        return pipeline_data

    def get_step(self, config):

        step_run_config = config.get("runconfig")
        pipeline_run_config = self.get_run_config(step_run_config)

        inputs_config = config.get("input")
        input_args = self.get_step_args(inputs_config, "input")
        input_pipeline_data = self.get_pipeline_data(inputs_config)
 
        outputs_config = config.get("output")
        output_args = self.get_step_args(outputs_config, "output")
        output_pipeline_data = self.get_pipeline_data(outputs_config)

        step_name = config.get("name")
        script_dir = config.get("script_dir")
        script_name = config.get("script_name")
        allow_reuse = config.get("allow_reuse").lower() == "true"

        arguments = input_args + output_args             

        step_type = config.get("type")

        if step_type == "PythonScriptStep":

            step = PythonScriptStep(
                name=step_name,
                source_directory=script_dir,
                script_name=script_name,
                arguments=arguments,
                inputs=input_pipeline_data,
                outputs=output_pipeline_data,
                runconfig=pipeline_run_config,
                allow_reuse=allow_reuse)
        
        return step