import os.path

from scratch_codes import ScratchCode
from db import Database
from utils import get_value, write_json_data, get_json_data


if __name__ == "__main__":

    mode = input('Введите 1, если хотите войти в режим генерации скретч-кодов.\n'
                 'Введите 2, если хотите войти в режим проверки скретч-кодов: ')

    hash_type = get_value('hash_type')
    hash_length = get_value('hash_length')
    first_serial_number = get_value('first_serial_number')
    first_serial_number_length = len(first_serial_number)

    scratch = ScratchCode()

    if mode == '1':
        filename = input('Введите имя файла, куда будут записаны скретч-коды: ')
        directory, file = os.path.split(filename)

        if not os.path.isdir(filename) and not directory or os.path.exists(directory):
            scratch_codes_count = get_value('scratch_codes_count')
            serial_number_length = len(str(int(first_serial_number) + scratch_codes_count).zfill(first_serial_number_length))
            scratch_codes = scratch.generate(serial_number_length, hash_type, hash_length, scratch_codes_count)
            write_json_data(scratch_codes, filename)

        else:
            print('Неправильное имя файла.')

    if mode == '2':
        filename = input('Введите имя файла, откуда будут взяты скретч-коды для проверки: ')

        if os.path.isfile(filename):
            scratch_codes = get_json_data(filename)
            serial_number_length = len(str(int(first_serial_number) + len(scratch_codes)).zfill(first_serial_number_length))
            checked_codes = scratch.check(scratch_codes, serial_number_length, hash_type, hash_length)

            db = Database()
            checked_codes = db.check_codes(checked_codes)

            print(checked_codes)

        else:
            print('Неправильное имя файла.')
