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
        is_valid, err_msg = is_resume_obj_valid(resume_obj, filename)
        if is_valid:
            return resume_obj, None
        else:
            error_messages.append(f"{filename} is not valid! {err_msg}")

    return None, error_messages


def is_resume_obj_valid(resume_obj, filename):
    def check(field, dtype, dtype_msg):
        assert resume_obj.get(field), f"{field} does not exist in {filename}"
        assert isinstance(
            resume_obj.get(field), dtype
        ), f"{field} should be {dtype_msg}"

    try:
        assert isinstance(resume_obj, dict), f"{filename} should be key-value pair"

        check("name", str, "a str")
        # assert resume_obj.get("name"), f"name does not exist in {filename}"
        # assert isinstance(resume_obj.get("name"), str), f"name should be of type str"

        check("contact", dict, "a dictionary")
        # assert resume_obj.get("contact"), f"contact does not exist in {filename}"
        # assert isinstance(resume_obj.get("contact"), dict), f"contact should be of type dict"

        check("education", list, "a list of dictionary")
        # assert resume_obj.get("education"), f"education does not exist in {filename}"
        # assert isinstance(resume_obj.get("education"), list), f"education should be a list of dictionary"

        check("links", dict, "a dictionary")
        # assert resume_obj.get("links"), f"links does not exist in {filename}"
        # assert isinstance(resume_obj.get("links"), dict), f"links should be a dictionary"

        for key, val in resume_obj["contact"].items():
            assert type(val) == str, f"Value of contact.{key} should be a str"

        for education in resume_obj["education"]:
            assert type(education) == dict, "Education entry should be a dictionary"
            for key, val in education.items():
                if key == "achievements":
                    assert (
                        type(education[key]) == list
                    ), f"Value of education.<entry>.{key} should be a list"
                    for achievement in education[key]:
                        print(achievement)
                        assert (
                            type(achievement) == str
                        ), f"Value of education.<entry>.{key}.<item> should be a str"
                else:
                    assert (
                        type(val) == str
                    ), f"Value of education.<entry>.{key} should be a str"

    except AssertionError as exc:
        return False, str(exc)
    else:
        return True, None
