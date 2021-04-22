import json


Class CfgParser:
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

    new_config = {}
    for k, v in config.items():
      secret = re.findall(self.secret_pattern, v)[0]
      new_config[k] = secrets.get(secret) or v

    return new_config