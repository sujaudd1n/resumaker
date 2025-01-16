import sys
import os
import yaml

CONFIG_FILENAME = "config.yml"

def load_config():
    """Returns config data by reading config.yml"""
    try:
        with open(CONFIG_FILENAME) as f:
            config = yaml.safe_load(f)
            if type(config) != dict:
                raise ValueError("config.yml is not valid")
            return config
    except FileNotFoundError:
        sys.exit(f"{CONFIG_FILENAME} can't be found!")

        

