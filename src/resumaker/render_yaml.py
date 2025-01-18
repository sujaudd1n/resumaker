import yaml
import sys

def get_pydict_from_yamls(filenames):
    if type(filenames) != list:
        filenames = [filenames]
    for filename in filenames:
        try:
            pydict = yamlfile_to_pydict(filename)
        except FileNotFoundError:
            continue
        except ValueError:
            sys.exit(f"{filename} is not valid!")
        else:
            return pydict
    sys.exit(f"{filenames} not found!")

def yamlfile_to_pydict(filename):
    """Converts filename into Python dict"""
    with open(filename) as f:
        pydict = yaml.safe_load(f)
        if type(pydict) != dict:
            raise ValueError
    return pydict
