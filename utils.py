import json


def get_config():
    with open('config.json') as f:
        data = json.load(f)
    return data

def get_value(key):
    data = get_config()
    return data[key]

def update_value(key, value):
    data = get_config()
    data[key] = value
    with open('config.json', 'w') as f:
        json.dump(data, f)

def generate_serial_number(serial_number_length):
    last_serial_number = int(get_value('last_serial_number'))
    serial_number = str(last_serial_number + 1).zfill(serial_number_length)
    update_value("last_serial_number", serial_number)
    return serial_number
