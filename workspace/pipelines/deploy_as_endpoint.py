from azureml.core import Workspace
from mlops.ml.endpoint import MlEndpoint
from mlops.util.cfgparser import CfgArgParser

def deploy_endpoint(workspace, config):
    endpoint = MlEndpoint(workspace=workspace)
    endpoint.build_pipeline(config=config)
    endpoint.deploy() 

    return endpoint.url

if __name__ == "__main__":

    parser = CfgArgParser("Deploy endpoint")
    parser.parse_args()
    
    config = parser.get_config()
    ws = Workspace.from_config()
    
    endpoint = deploy_endpoint(ws, config)

    print(f"endpoint: {endpoint}")