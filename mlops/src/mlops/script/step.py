import argparse
import json
from azureml.core import Dataset
from azureml.core import Model
from azureml.core.datastore import Datastore
from functools import wraps
from mlops.util.decorators import mlrun

class StepArgParser():

    ARG_TYPE_NAMED_INPUT = "named_input"
    ARG_TYPE_PIPELINE_DATA = "pipeline_data"
    ARG_TYPE_REG_DATASET = "registered_dataset"
    ARG_TYPE_REG_MODEL = "registered_model"
    ARG_TYPE_NAMED_INPUT_KEY = "named_input_key"

    INPUT_ARGS = {
        ARG_TYPE_NAMED_INPUT: {
            "flag": "-n",
            "type": str,
            "dest": "input_datasets",
            "help": "Input Dataset object",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_PIPELINE_DATA: {
            "flag": "-p",
            "type": str,
            "dest": "input_pipeline_data_dirs",
            "help": "Input PipelineData directory",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_REG_DATASET: {
            "flag": "-d",
            "type": str,
            "dest": "input_reg_datasets",
            "help": "Input registered dataset",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_REG_MODEL: {
            "flag": "-m",
            "type": str,
            "dest": "input_reg_models",
            "help": "Input registered model",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_NAMED_INPUT_KEY:{
            "flag": "-i",
            "type": str,
            "dest": "named_input_keys",
            "help": "Named input label",
            "required": False,
            "action": 'append'
        }
    }

    OUTPUT_ARGS = {
        ARG_TYPE_PIPELINE_DATA: {
            "flag": "-P",
            "type": str,
            "dest": "output_pipeline_data_dirs",
            "help": "Output PipelineData directory",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_REG_DATASET: {
            "flag": "-D",
            "type": str,
            "dest": "output_reg_datasets",
            "help": "Output registered dataset",
            "required": False,
            "action": 'append'
        },
        ARG_TYPE_REG_MODEL: {
            "flag": "-M",
            "type": str,
            "dest": "output_reg_models",
            "help": "Output registered model",
            "required": False,
            "action": 'append'
        }
    }

    def __init__(self, description=None):
        self.description = description
    
    def parse_args(self):

        parser = argparse.ArgumentParser(description=self.description)

        for args in [self.INPUT_ARGS, self.OUTPUT_ARGS]:
            for k, v in args.items():
                v_args = v.copy()
                first_arg = v_args.pop("flag")

                parser.add_argument(first_arg, **v_args)

        return parser.parse_args()
        

class StepDecorator():

    OUTPUT_FORMAT = "parquet"

    def __init__(self, 
                 input_datasets=[],
                 named_input_keys=[],
                 input_pipeline_data_dirs=[],
                 input_reg_datasets=[],
                 input_reg_models=[],
                 output_pipeline_data_dirs=[],
                 output_reg_datasets=[],
                 output_reg_models=[]):

        def config_to_json_list(config):
            return list(map(lambda x: json.loads(x), config or []))

        self.input_datasets = input_datasets
        self.named_input_keys = named_input_keys
        self.input_pipeline_data_dirs = config_to_json_list(input_pipeline_data_dirs)
        self.input_reg_datasets = config_to_json_list(input_reg_datasets)
        self.input_reg_models = config_to_json_list(input_reg_models)
        self.output_pipeline_data_dirs = config_to_json_list(output_pipeline_data_dirs)
        self.output_reg_datasets = config_to_json_list(output_reg_datasets)
        self.output_reg_models = config_to_json_list(output_reg_models)

    def __call__(self, func):
        
        @mlrun
        @wraps(func)
        def inner(*args, **kwargs):
            run = kwargs.get("run")
            ws = run.experiment.workspace

            def register_model(model_name, model_path):
                model_config = next(iter(filter(lambda x: x["name"] == model_name, self.output_reg_models)))
                
                tags = model_config.get("tags")
                description = model_config.get("description")

                Model.register(workspace=ws, model_path=model_path, model_name=model_name, tags=tags, description=description)

            def register_dataset(dataset_name, dataframe):
                dataset_config = next(iter(filter(lambda x: x["name"] == dataset_name, self.output_reg_datasets)))
                
                datastore = dataset_config.get("datastore") or "default"
                description = dataset_config.get("description")
                tags = dataset_config.get("tags")

                if datastore == "default":
                    ds = ws.get_default_datastore()
                else:
                    ds = Datastore.get(workspace=ws, datastore_name=datastore)

                target_path = f'experiment/{run.experiment.name}/run/{run.number}/out/{dataset_name}'

                default_output_dataset_tags = {
                    "format": self.OUTPUT_FORMAT,  # Dataset.Tabular.register_pandas_dataframe always writes a parquet
                    "experiment": run.experiment.name,
                    "run": run.number
                }

                output_dataset_tags = {**default_output_dataset_tags, **tags}
                
                Dataset.Tabular.register_pandas_dataframe(
                    dataframe, 
                    target=(ds, target_path), 
                    name=dataset_name, 
                    description=description,
                    tags=output_dataset_tags
                )

            dataframes = {}
            for i, d in enumerate(self.input_datasets or []):
                dkey = self.named_input_keys[i]
                dataframes[dkey] = run.input_datasets[dkey].to_pandas_dataframe()
            
            for d in self.input_reg_datasets or []:
                dname = d["name"]
                dver = d.get("version")
                if dver == "latest":
                    dver = None

                dataframes[dname] = Dataset.get_by_name(ws, name=dname, version=dver).to_pandas_dataframe()

            kwargs["dataframes"] = dataframes

            models = {}
            for m in self.input_reg_models or []:
                mname = m["name"]
                mver = m.get("version")
                if mver == "latest":
                    mver = None

                models[mname] = Model.get_model_path(model_name=mname, version=mver, _workspace=ws)
            
            kwargs["models"] = models

            pipeline_data_dirs = []
            for p in self.input_pipeline_data_dirs or []:
                pipeline_data_dirs.append(p["name"])

            kwargs["pipeline_data_dirs"] = pipeline_data_dirs

            register_dataframes, register_models = func(*args, **kwargs)

            for k in register_dataframes or {}:
                v = register_dataframes[k]
                register_dataset(dataset_name=k, dataframe=v)

            for k in register_models or {}:
                v = register_models[k]
                register_model(model_name=k, model_path=v)

        return inner
