import sys
import os
import yaml

def read_file_txt(filename):
    with open(filename) as f:
        return f.read()

def render_yaml_txt(yaml_txt):
    return yaml.safe_load(yaml_txt)

def is_dict(obj):
    return type(obj) == dict

def validate_yaml_txt_as_dict(yaml_txt):
    obj = render_yaml_txt(yaml_txt)
    if is_dict(obj):
        return obj
    raise ValueError(f"{obj} is not a dict")

'''
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
'''