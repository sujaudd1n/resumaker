import sys
import os
import yaml


def read_file_txt(filename):
    """Read filename and return its text"""
    with open(filename) as f:
        return f.read()


def render_yaml_txt(yaml_txt):
    "Render and return yaml_txt"
    return yaml.safe_load(yaml_txt)
