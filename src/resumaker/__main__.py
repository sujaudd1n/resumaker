import argparse
from .utils import get_config
from .render_yaml import get_pydict_from_yamls

def main():
    args = get_args()
    config = get_config()
    if args.f:
        resume_filename = args.f
    else:
        resume_filename = config["RESUME_YAML_FILENAME"]
    resume_pydict = get_pydict_from_yamls(resume_filename)
    print(resume_pydict)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Filename of yaml file of resume data")
    args = parser.parse_args()
    return args
if __name__ == "__main__":
    main()