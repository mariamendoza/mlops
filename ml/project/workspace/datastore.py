import argparse
import json
import logging
from project.util import CfgParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup(config, secrets):
  json_config = json.loads(config)
  cfgparser = CfgParser()
  cfg = cfgparser.parse(config, secrets)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Setup workspace datastores')
  parser.add_argument('--config', type=str, help='json config file')
  parser.add_argument('--secrets', type=str, help='map of secrets')
  args = parser.parse_args()
  cfg = args.config
  secrets = args.secrets
  setup(cfg, secrets)