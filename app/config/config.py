import os

import yaml


class Configuration(object):
    """
    Configuration class for loading configuration options
    """

    def __init__(self):
        self.config = {}

    def load_config(self):
        """
        Loads the YAML config file as a dict
        """
        config_location = os.environ.get("CONFIG_PATH")
        if not config_location:
            raise EnvironmentError(
                "Please set CONFIG_PATH as an environment variable for the path to the "
                "configuration file"
            )

        with open(config_location, "r") as config_file:
            self.config = yaml.safe_load(config_file)

    def get(self, key, default=None):
        """
        Get a value from the configuration based on the key
        """
        value = self.config
        for k in key.split("."):
            try:
                value = value[k]
            except KeyError:
                return default

        return value


CONFIG = Configuration()
CONFIG.load_config()

get = CONFIG.get
