from mlops.script.step import StepArgParser
from mlops.script.step import StepDecorator

def run_step(**kwargs):

    tags = {"step_script": __file__}

    @StepDecorator(**kwargs)
    def step(run=None, 
             dataframes=None, 
             models=None, 
             pipeline_data_dirs=None):
        """
        Docstrings TODO
        """

        register_dataframes = {}
        register_models = {}

        # TODO

        return register_dataframes, register_models

    step()

if __name__ == "__main__":

    step_description = "replace this"
    parser = StepArgParser(step_description)
    args = parser.parse_args()
    
    keyword_args = vars(args)
    run_step(**keyword_args)
