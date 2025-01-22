import yaml
import sys
from .utils import (
    read_file_txt,
    render_yaml_txt,
)

def get_resume_obj(filenames):
    """
    Return resume dict by rendering first successful filename
    """
    error_messages = []
    for filename in filenames:
        try:
            resume_yaml_txt = read_file_txt(filename)
        except FileNotFoundError:
            error_messages.append(f"{filename} is not found!")
            continue

        resume_obj = render_yaml_txt(resume_yaml_txt)
        if is_resume_obj_valid(resume_obj):
            return resume_obj
        else:
            error_messages.append(f"{filename} is not valid!")

    for error_message in error_messages:
        print(error_message)

    sys.exit(f"Could not render {filenames} into valid resume object!")

def is_resume_obj_valid(resume_obj):
    return isinstance(resume_obj, dict)