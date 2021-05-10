import argparse
import json
import re
from mlops.util import ArgParser


class CfgParser:
    def __init__(self):
        self.secret_pattern = r"\$:(.+)"

    def read(self, configfile):
        """
        Read config file into json.

        Args:
            configfile (string): json configuration file
        
        Returns:
            dict: json configuration as read from file
        """

        with open(configfile, 'r') as f:
            lines = f.readlines()
          
        lines = ''.join(lines)
        config = json.loads(lines)

        return config
    
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
                new_config[k] = parsed

            return new_config

        else:
            secret = next(iter(re.findall(self.secret_pattern, config)), None)
            return secrets.get(secret) or config


class CfgArgParser(ArgParser):

    def __init__(self, description=None):
        super().__init__(description)

    def build_parser(self):
        super().build_parser()
        self.parser.add_argument('-f', type=str, dest="configfile", help='json config file', required=True)
        self.parser.add_argument('-s', type=str, dest="secretsmap", help='map of secrets', default={})
        
    def get_config(self):
        configfile = self.args.configfile
        secretsmap = self.args.secretsmap
        
        cfgparser = CfgParser()
        json_config = cfgparser.read(configfile)

        if secretsmap:
            secrets = json.loads(secretsmap.replace("'", '"'))
            config = cfgparser.parse(json_config, secrets)
        else:
            config = json_config
        
        return config