import argparse
import json

from resumaker.config import get_config
from resumaker.utils import is_resume_valid, common_fields
from resumaker.render_resume import *
from resumaker.resume import Resume
from resumaker.__about__ import __version__


def main():
    parser = get_parser()
    config = get_config()

    args = parser.parse_args()

    if args.filenames:
        filenames = args.filenames
        if type(filenames) != list:
            filenames = [filenames]
        resume_filenames = filenames
    else:
        resume_filenames = config["RESUME_FILENAME"]

    resume_target = args.target if args.target else None

    result, errors = get_resume_obj(resume_filenames)

    if result:
        complete_resume_obj = result
    else:
        for error in errors:
            print(error)
        sys.exit(f"Could not render {resume_filenames} into valid resume object!")

    is_valid, msg = is_resume_valid(complete_resume_obj)
    if not is_valid:
        sys.exit(msg)

    common = {
        "name": complete_resume_obj.get("name"),
        "location": complete_resume_obj.get("location"),
        "contact": complete_resume_obj.get("contact"),
        "education": complete_resume_obj.get("education"),
        "links": complete_resume_obj.get("links"),
    }

    given_targets = [
        key for key in complete_resume_obj.keys() if key not in common_fields
    ]

    print(given_targets)

    if resume_target:
        if resume_target in given_targets:
            target_details = [complete_resume_obj[resume_target] | common]
        else:
            sys.exit("Target is not in the resume")
    else:
        target_details = []
        for target in given_targets:
            target_details.append(
                complete_resume_obj[target] | {"target_name": target} | common
            )

    def build_name(target):
        user_name = target["name"].replace(" ", "").lower()
        target_name = target["target_name"]
        return f"{user_name}-{target_name}"

    for target in target_details:
        resume = Resume(
            target["name"],
            target["location"],
            target["contact"],
            target["summary"],
            target["education"],
            target["links"],
            target["skills"],
            target["work-experience"],
            order=config["ORDER"],
        )
        resume.build(build_name(target))
        # print(json.dumps(complete_resume_obj, indent=2))


def get_parser():
    parser = argparse.ArgumentParser(
        prog="resumaker",
        description="Build multi-profile ATS friendly resume from a single YAML file.",
        epilog="Thank you for using resumaker.\n"
        "To contribute, please visit https://github.com/sujaudd1n/resumaker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--filename",
        metavar="filename",
        dest="filenames",
        help="Filename of resume yaml file.",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="target",
        dest="target",
        help="Select target such as devops or AI in your resume",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


if __name__ == "__main__":
    main()
