import sys
import os
import yaml

from .utils import (
    read_file_txt,
    render_yaml_txt
)

CONFIG_FILENAME = "config.yml"
default_configs = {"RESUME_FILENAME": ["resume.yml", "resume.yaml"]}

def get_config():
    """
    Return config data by overwriting default_configs
    by reading config.yml if exists else default_configs
    """
    try:
        user_config_txt = read_file_txt(CONFIG_FILENAME)
    except FileNotFoundError:
        return default_configs
    else:
        return manage_user_config_txt(user_config_txt)


def manage_user_config_txt(user_config_txt):
    """
    if config_obj is valid, merge it with default_configs
    and return else return default_configs
    """
    user_config_obj = render_yaml_txt(user_config_txt)
    if is_config_valid(user_config_obj):
        return merge_user_config_with_defaults(user_config_obj)
    else:
        print("config.yml is not valid! Using default configs.")
        return default_configs

def is_config_valid(config_obj):
    """
    config_obj has to be a dict.
    Each value in key: value has to be a str or list
    """
    if not isinstance(config_obj, dict):
        return False
    for _, val in config_obj.items():
        if not isinstance(val, list) and not isinstance(val, str):
            return False
    return True

def merge_user_config_with_defaults(user_config_obj):
    """
    Overwrite default_configs with user_config_obj.
    return default_config
    """
    for config in user_config_obj:
        if config in default_configs:
            user_config_value = user_config_obj[config]
            default_configs[config] = user_config_value if type(user_config_value) == list else [user_config_value]
        else:
            print(f"{config} is not supported!")
    return default_configs
