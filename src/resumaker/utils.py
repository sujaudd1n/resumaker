import sys
import os
import yaml

CONFIG_FILENAME = "config.yml"

default_configs = {"RESUME_YAML_FILENAME": ["resume.yml", "resume.yaml"]}


def load_config():
    """Load config data by reading config.yml
    If config.yml is valid (a dict), it return it.
    else sys.exit
    """
    try:
        with open(CONFIG_FILENAME) as f:
            return f.read()
    except FileNotFoundError:
        return ""

def render_yaml(config_txt):
    return yaml.safe_load(config_txt)

def get_rendered_config():
    config_txt = load_config()
    config_obj = render_yaml(config_txt)

def is_config_valid(config):
    return type(config) == dict

def get_valid_user_config():
    config = get_rendered_config()
    if not is_config_valid(config):
        raise ValueError("config.yml is not valid!")
    else:
        return config
    

def get_config():
    """Return config data by overwriting default_configs
    by reading config.yml
    """
    user_configs = get_valid_user_config()
    for config in user_configs:
        if config in default_configs:
            default_configs[config] = user_configs[config]
        else:
            print(f"{config} is not supported!")
    return default_configs