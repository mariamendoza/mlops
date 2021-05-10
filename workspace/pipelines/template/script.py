import argparse
import os
from azureml.core import Dataset
from functools import wraps
from mlops.script.step import StepArgParser
from mlops.script.step import StepDecorator
from mlops.util.decorators import mlrun


def run_step(input_name, output_dir=None, output_dataset_name=None):

    output_file_basename = os.path.splitext(__file__)[0]
    output_dataset_description = f"output dataset for {__file__} script step"
    output_dataset_tags = {"step_script": __file__}

    @StepDecorator(input_name=input_name, 
                   output_dir=output_dir, 
                   output_dataset_name=output_dataset_name,
                   output_file_basename=output_file_basename, 
                   output_dataset_description=output_dataset_description,
                   output_dataset_tags=output_dataset_tags)
    def step(df=None, run=None):
        """
        Implement step here.

        Retain function signature and always return the processed output df.
        Actual call to step does not need to pass any arguments.
        If arguments are passed, they are overwritten by decorators.

        StepDecorator creates the dataframe (df) that is passed to this function.
        StepDecorator also applies mlrun decorator.
        mlrun decorator passes the run context using run argument.
        """

        # TODO

        return df

    step()

if __name__ == "__main__":

    step_description = "replace this"
    parser = StepArgParser(step_description)
    args = parser.parse_args()
    
    run_step(input_name=args.input_name, 
             output_dir=args.output_dir, 
             output_dataset_name=args.output_dataset_name)
