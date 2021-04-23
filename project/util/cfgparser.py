import json
import re

class CfgParser:
  def __init__(self):
    self.secret_pattern = r"\$:(.+)"

  def parse(self, config, secrets):
    """
    Applies secrets to config.

    Args:
      config (dict): as read from config file
      secrets (dict): secrets to be applied to config

    Returns:
      dict: config with secrets applied
    """

    if isinstance(config, list):
      items = []
      
      for item in config:
        parsed = self.parse(item, secrets)
        items.append(parsed)
      
      return items

    elif isinstance(config, dict):
      new_config = {}

      for k, v in config.items():
        parsed = self.parse(v, secrets)
      
        if v == parsed:
          secret = next(iter(re.findall(self.secret_pattern, v)), None)
          new_config[k] = secrets.get(secret) or v
        else:
          new_config[k] = parsed

      return new_config

    else:
      return config