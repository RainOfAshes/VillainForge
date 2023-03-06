from typing import Union, List, Dict

import yaml


def read_yaml(filename: str) -> Union[List, Dict]:
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    return data
