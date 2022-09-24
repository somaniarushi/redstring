from pathlib import Path
import json

def sanitize_for_root(filepath):
    """
    In redstring, the file must be stated with respect to the root directory.
    """
    cwd = Path(__file__).parent
    sanitized_path = (cwd / filepath).resolve()
    return sanitized_path

def dump_json_to_file(dict, store_path):
    store_path = sanitize_for_root(store_path)
    with open(store_path, 'w') as json_file:
        json.dump(dict, json_file)

def get_json_from_file(store_path):
    store_path = sanitize_for_root(store_path)
    with open(store_path, 'r') as json_file:
        data = json.load(json_file)
    return data

