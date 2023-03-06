import os, configparser, json
import logging
logger = logging.getLogger("flask-app")

dir_path = os.path.dirname(os.path.realpath(__file__))
from utils.json_util import JsonUtils

class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._config = cls.load_config()
        return cls._instance

    @staticmethod
    def load_config():
        try:
            # Determine the environment
            if 'ENV' in os.environ:
                env = os.environ['ENV']
            else:
                env = 'dev'

            # Load the default configuration file
            with open(f'{dir_path}/default.json', 'r') as f:
                default_configs = json.load(f)

            # Load the environment-specific configuration file
            with open(f'{dir_path}/{env}.json', 'r') as f:
                env_config = json.load(f)

            # Merge the default and dynamic properties.
            merged_configs = JsonUtils.merge_json(default_configs, env_config)
            
            return merged_configs

        except (FileNotFoundError, json.JSONDecodeError, configparser.Error) as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    @staticmethod
    def get_config():
        if ConfigLoader._config is None:
            ConfigLoader._config = ConfigLoader.load_config()
        return ConfigLoader._config