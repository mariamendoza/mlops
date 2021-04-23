import argparse
import json
import logging

from azureml.core import Datastore, Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from project.util.auth import get_service_principal
from project.util.cfgparser import CfgParser
from msrest.exceptions import HttpOperationError

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

def is_datastore_exists(workspace, name):
  try:
    ds = Datastore.get(workspace, name)
    return True
  except HttpOperationError:
    return False

def register_datastore(workspace, ds_config):
  ds_name = ds_config.get("name")

  if not is_datastore_exists(workspace, ds_name):
    Datastore.register_azure_blob_container(
      workspace=workspace,
      datastore_name=ds_name,
      account_name=ds_config.get("account_name"),
      container_name=ds_config.get("container_name"),
      account_key=ds_config.get("account_key"),
      create_if_not_exists=ds_config.get("create_if_not_exists")
    )

def get_workspace(config, service_principal):
  ws_config = config.get("workspace")
  ws_name = ws_config.get("name")
  ws_subscription_id = ws_config.get("subscription_id")
  ws_resource_group = ws_config.get("resource_group")

  ws = Workspace.get(ws_name, 
                     subscription_id=ws_subscription_id,
                     resource_group=ws_resource_group,
                     auth=service_principal)

  return ws

def setup(service_principal, configfile, secretsmap=None):

  with open(configfile, 'r') as f:
    lines = f.readlines()
    
  lines = ''.join(lines)
  json_config = json.loads(lines)

  if secretsmap:
    secrets = json.loads(secretsmap)
    cfgparser = CfgParser()
    config = cfgparser.parse(json_config, secrets)
  else:
    config = json_config
  
  ws = get_workspace(config, service_principal)
  datastores = config.get("workspace").get("datastores")

  for ds_config in datastores:
    register_datastore(ws, ds_config)

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(description='Setup workspace datastores')
  parser.add_argument('-f', type=str, dest="configfile", help='json config file', required=True)
  parser.add_argument('-s', type=str, dest="secretsmap", help='map of secrets', default={})

  args = parser.parse_args()
  
  cfg = args.configfile
  secretsmap = args.secretsmap

  service_principal = get_service_principal()
  setup(service_principal, cfg, secretsmap)