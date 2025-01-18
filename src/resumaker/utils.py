import sys
import os
import yaml

CONFIG_FILENAME = "config.yml"

default_configs = {
    "RESUME_YAML_FILENAME": ["resume.yml", "resume.yaml"]
}

def load_config():
    """Load config data by reading config.yml
       If config.yml is valid (a dict), it return it.
       else sys.exit
    """
    try:
        with open(CONFIG_FILENAME) as f:
            config = yaml.safe_load(f)
            if type(config) != dict:
                sys.exit("config.yml is not valid.")
            return config
    except FileNotFoundError:
        return {}
        
def get_config():
    """Return config data by overwriting default_configs
       by reading config.yml 
    """
    user_configs = load_config()
    for config in user_configs:
        if config in default_configs:
            default_configs[config] = user_configs[config]
        else:
            print(f"{config} is not supported!")
    return default_configs
