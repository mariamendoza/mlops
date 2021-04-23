import argparse
import json
import logging

from azureml.core import Datastore, Workspace
from project.util.cfgparser import CfgParser

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

def is_datastore_exists(workspace, name):
  try:
    ds = Datastore.get(workspace, name)
    return True
  except HttpOperationError:
    return False

def register_datastore(workspace, datastore_config):
  ds_name = ds_config.get("name")

  if not is_datastore_exists(ws, ds_name):
    print(datastore_config)
    # Datastore.register_azure_blob_container(
    #   workspace=ws,
    #   datastore_name=ds_name,
    #   account_name=ds_config.get("account_name"),
    #   container_name=ds_config.get("container_name"),
    #   account_key=ds_config.get("account_key"),
    #   create_if_not_exists=ds_config.get("create_if_not_exists")
    # )

def get_workspace(config):
  ws_config = cfg.get("workspace")
  ws_name = ws_config.get("name")
  ws_subscription_id = ws_config.get("subscription_id")
  ws_resource_group = ws_config.get("resource_group")

  ws = Workspace.get(ws_name, 
                     subscription_id=ws_subscription_id,
                     resource_group=ws_resource_group)

  return ws

def setup(configfile, secrets):

  with open(configfile, 'r') as f:
    config = f.readlines()
    
  config = ''.join(config)
  json_config = json.loads(config)
  cfgparser = CfgParser()
  cfg = cfgparser.parse(config, secrets)

  ws = get_workspace(config)
  datastores = ws_config.get("datastores")

  for ds_config in datastores:
    register_datastore(ws, ds_config)

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(description='Setup workspace datastores')
  parser.add_argument('-f', type=str, dest="configfile", help='json config file', required=True)
  parser.add_argument('-s', type=str, dest="secrets", help='map of secrets', default={})

  args = parser.parse_args()
  
  cfg = args.configfile
  secrets = args.secrets

  print(json.loads(secrets))
  
  setup(cfg, secrets)