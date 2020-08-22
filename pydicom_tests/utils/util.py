import json
import os

_FILE_FOLDER_PATH = '../tests/files/'

def read_json(json_path):
    with open(os.path.relpath(f'{_FILE_FOLDER_PATH}{json_path}'), 'r') as f:
        return json.load(f)


def read_file(filename):
    return os.path.relpath(f'{_FILE_FOLDER_PATH}{filename}')
