from azureml.core import Dataset
from azureml.core import Environment
from azureml.core.compute import ComputeTarget
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep


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

        dataset = Dataset.get_by_name(
            workspace=self.workspace, 
            name=name, 
            version=version or "latest" )
        
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

        conda_dep = CondaDependencies()
        conda_dep.add_pip_package(whl_url)
        environment.python.conda_dependencies=conda_dep

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

    def get_step(self, config):

        step_run_config = config.get("runconfig")
        pipeline_run_config = self.get_run_config(step_run_config)

        input_dataset_config = config.get("input_dataset")
        as_named_input = input_dataset_config.get("as_named_input")
        input_dataset = self.get_dataset(input_dataset_config)

        step_name = config.get("name")
        script_dir = config.get("script_dir")
        script_name = config.get("script_name")
        output_dir = config.get("output_dir")
        output_dataset_name = config.get("output_dataset_name")
        allow_reuse = config.get("allow_reuse").lower() == "true"

        arguments = ['-d', input_dataset.as_named_input(as_named_input),
                    '-i', as_named_input,
                    '-n', output_dataset_name,
                    '-o', output_dir]             

        step_type = config.get("type")

        if step_type == "PythonScriptStep":

            step = PythonScriptStep(
                name=step_name,
                source_directory=script_dir,
                script_name=script_name,
                arguments=arguments,
                runconfig=pipeline_run_config,
                allow_reuse=allow_reuse)
        
        return step