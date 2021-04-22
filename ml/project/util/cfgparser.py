import json

Class CfgParser:
  def __init__(self):
    self.secret_pattern = r"\$:(.+)"

  def _recurse_keys(config):
    """
    Creates a nested list of keys extracted from config json/dict.
    Called recursively.

    Args:
      config (dict): json/dict config
    
    Returns:
      list: nested list of keys
    """

    keys = []
    for k, v in config.items():





  def parse(self, config, secrets):
    """
    Applies secrets to config.

    Args:
      config (dict): as read from config file
      secrets (dict): secrets to be applied to config

    Returns:
      dict: config with secrets applied
    """

    new_config = {}
    for k, v in config.items():
      secret = re.findall(self.secret_pattern, v)[0]
      new_config[k] = secrets.get(secret) or v

    return new_config

Class WorkspaceCfgParser(CfgParser):

  _CONFIG_TEMPLATE = { 
    "workspace":
      {
        "name": "",
        "subscription_id": "string",
        "resource_group": "string",
        "datastores": [
          {
            "name": "string",
            "container_name": "string",
            "account_name": "string",
            "account_key": "string",
            "create_if_not_exists": "True",
            "subscription_id": "string",
            "resource_group": "string"
          },
          {
            "name": "string",
            "container_name": "string",
            "account_name": "string",
            "account_key": "string",
            "create_if_not_exists": "True",
            "subscription_id": "string",
            "resource_group": "string"
          }
        ]
      }
    }

  def __init__(self):
    super().__init__()
  
  def validate(self):


