import json
import sys


CONFIG_FILE_PATH = 'config.json'

def get_json_data(path):
    try:
        with open(path) as f:
            data = json.load(f)
        return data
    except ValueError:
        print('В файле содержатся данные в неправильном формате.')
        sys.exit()

def write_json_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def get_value(key):
    data = get_json_data(CONFIG_FILE_PATH)
    return data[key]

def update_value(key, value):
    data = get_json_data(CONFIG_FILE_PATH)
    data[key] = value
    write_json_data(data, CONFIG_FILE_PATH)
