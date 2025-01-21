import sys
import os
import yaml

CONFIG_FILENAME = "config.yml"
default_configs = {"RESUME_YAML_FILENAME": ["resume.yml", "resume.yaml"]}

def get_config():
    """Return config data by overwriting default_configs
    by reading config.yml
    """
    try:
        user_config_txt = load_config()
    except FileNotFoundError:
        return default_configs
    else:
        return manage_user_config_txt(user_config_txt)


def load_config():
    """Load config data by reading config.yml
    If config.yml is valid (a dict), it return it.
    else sys.exit
    """
    with open(CONFIG_FILENAME) as f:
        return f.read()

def manage_user_config_txt(user_config_txt):
    user_config_obj = validate_config_txt(user_config_txt)
    return merge_user_config_with_defaults(user_config_obj)

def merge_user_config_with_defaults(user_config_obj):
    for config in user_config_obj:
        if config in default_configs:
            user_config_value = user_config_obj[config]
            default_configs[config] = user_config_value if type(user_config_value) == list else [user_config_value]
        else:
            print(f"{config} is not supported!")
    return default_configs

def validate_yaml_txt(yaml_txt):
    pyobj = yaml.safe_load(yaml_txt)
    if type(pyobj) != dict:
        raise ValueError("Rendered YAML is not a dict.")
    return pyobj
    

def validate_config_txt(txt):
    config_obj = yaml_to_pyobj(txt)
    if type(config_obj) == dict:
        return config_obj
    else:
        print("config.yml is not valid! Using default configs.")
        return {}

def yaml_to_pyobj(yaml_txt):
    return yaml.safe_load(yaml_txt)