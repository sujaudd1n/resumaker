import argparse
import json

from .utils import get_config
from .render_yaml import get_pydict_from_yamls
from .data_structures import Resume


def main():
    args = get_args()
    config = get_config()

    if args.f:
        resume_filename = args.f
    else:
        resume_filename = config["RESUME_YAML_FILENAME"]

    target = args.t if args.t else "default"

    resume_pydict = get_pydict_from_yamls(resume_filename)

    if target in resume_pydict:
        summary = resume_pydict[target]["summary"]
    else:
        summary = resume_pydict["summary"]

    resume = Resume(
        resume_pydict["name"],
        resume_pydict["location"],
        resume_pydict["contact"],
        summary
    )
    resume.build()

    # print(json.dumps(resume_pydict, indent=2))


def get_args():
    parser = argparse.ArgumentParser(
        prog="resumaker",
        description="Build multi-profile ATS friendly resume from a single YAML file.",
        epilog="Thank you for using resumaker.\n"
               "To contribute, please visit https://github.com/sujaudd1n/resumaker.",
        formatter_class = argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", help="Filename of yaml file of resume data")
    parser.add_argument("-t", help="Targeted resume")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
