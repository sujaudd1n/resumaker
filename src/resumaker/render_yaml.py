import yaml
import sys
from .utils import validate_yaml_txt


def get_resume_obj(filenames):
    "Return resume dict by rendering first successful filename"
    error_messages = []
    for filename in filenames:
        try:
            resume_yaml_txt = read_file_txt(filename)
        except FileNotFoundError:
            error_messages.append(f"{filename} is not found!")
            continue

        try:
            resume_obj = validate_yaml_txt_as_dict(resume_yaml_txt)
        except:
            error_messages.append(f"{filename} is not valid!")
        else:
            return resume_obj

    for error_message in error_messages:
        print(error_message)

    sys.exit(f"Could not render {filenames} into valid resume object!")

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