import argparse
import os
from azureml.core import Dataset
from functools import wraps
from mlops.util.decorators import mlrun

class StepArgParser():

    def __init__(self, description=None):
        self.description = description
    
    def parse_args(self):

        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('-d', type=str, dest="dataset", 
                            help='Azure ML dataset', 
                            required=True)
        parser.add_argument('-i', type=str, dest="input_name", 
                            help='Dataset as named input name', 
                            required=True)
        parser.add_argument('-o', type=str, dest="output_dir",
                            help='Output directory',
                            required=False)
        parser.add_argument('-n', type=str, dest="output_dataset_name",
                            help="Register output as dataset with name",
                            required=False)
        
        return parser.parse_args()
        

class StepDecorator():

    OUTPUT_FORMAT = "parquet"

    def __init__(self, 
                 input_name, 
                 output_dir=None, 
                 output_dataset_name=None,
                 output_file_basename=None, 
                 output_dataset_description=None,
                 output_dataset_tags={}):

        self.input_name = input_name
        self.output_dir = output_dir
        self.output_dataset_name = output_dataset_name

        self.output_file_basename = output_file_basename
        self.output_filename = f"{self.output_file_basename}.{self.OUTPUT_FORMAT}"

        self.output_dataset_description = output_dataset_description
        self.output_dataset_tags = output_dataset_tags

    def __call__(self, func):
        
        @mlrun
        @wraps(func)
        def inner(*args, **kwargs):
            run = kwargs.get("run")
            df = run.input_datasets[self.input_name].to_pandas_dataframe()
            kwargs["df"] = df
            output_df = func(*args, **kwargs)

            if self.output_dir:
                os.makedirs(self.output_dir, exist_ok=True)
                output_file_path = os.path.join(self.output_dir, self.output_filename)

                output_df.to_parquet(output_file_path, index=False)

            if self.output_dataset_name:
                ws = run.experiment.workspace
                ds = ws.get_default_datastore()

                target_path = f'experiment/{run.experiment.name}/run/{run.number}/out/{self.output_filename}'

                default_output_dataset_tags = {
                    "format": self.OUTPUT_FORMAT,
                    "experiment": run.experiment.name,
                    "run": run.number
                }

                output_dataset_tags = {**default_output_dataset_tags, **self.output_dataset_tags}
                
                output_dataset = Dataset.Tabular.register_pandas_dataframe(
                    output_df, 
                    target=(ds, target_path), 
                    name=self.output_dataset_name, 
                    description=self.output_dataset_description,
                    tags=output_dataset_tags
                )

        return inner