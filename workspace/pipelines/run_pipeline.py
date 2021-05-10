from azureml.core import Workspace
from mlops.ml.pipeline import MlPipeline
from mlops.util.cfgparser import CfgArgParser

def run_pipeline(workspace, name, config):
    pipeline = MlPipeline(workspace=workspace)
    pipeline.from_config(config).submit(name)

    print(f"{name} submitted")

if __name__ == "__main__":

    parser = CfgArgParser("Run pipeline")
    parser.build_parser()
    parser.add_argument('-n', type=str, dest="name", help="pipeline experiment name", required=True)
    parser.parse_args()
    
    name = parser.args.name
    config = parser.get_config()
    ws = Workspace.from_config()
    
    run_pipeline(workspace=ws, name=name, config=config)