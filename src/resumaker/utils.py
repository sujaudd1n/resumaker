import sys
import os
import yaml

common_fields = {
    "name": str,
    "location": str,
    "contact": dict,
    "education": list,
    "links": dict,
    "skills": dict,
}


def read_file_txt(filename):
    """Read filename and return its text"""
    with open(filename) as f:
        return f.read()


def render_yaml_txt(yaml_txt):
    "Render and return yaml_txt"
    return yaml.safe_load(yaml_txt)


def is_resume_valid(resume_obj):
    try:
        assert isinstance(resume_obj, dict), "Resume should be a dictionary"
        # check each common-field's type is valid if present
        for field, dtype in common_fields.items():
            if field in resume_obj:
                assert isinstance(
                    resume_obj[field], dtype
                ), f"{field} should be a {dtype}"
    except AssertionError as exc:
        return False, str(exc)
    return True, None


def is_config_valid(config_obj):
    """
    config_obj has to be a dict.
    Each value in key: value has to be a str or list
    """
    try:
        assert isinstance(config_obj, dict), "config.yml should be convertible to Python dict"
        for _, val in config_obj.items():
            assert isinstance(val, list) or isinstance(val, str), "Value of config has to be str or list of str"
    except AssertionError as exc:
        return False, str(exc)
    return True, None
