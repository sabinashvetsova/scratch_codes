from scratch_codes import ScratchCode
import sys
from utils import get_value


if __name__ == "__main__":

    serial_number_length = int(input('Введите длину серийного номера: '))

    hash_types = get_value('hash_functions')
    delimiter = ', '
    hash_type = input(f'Выберите одну из хэш-функций ({delimiter.join(hash_types)}): ')
    if hash_type not in hash_types:
        print('Неправильный выбор')
        sys.exit()

    hash_length = int(input('Введите количество знаков, которые берутся от хэш-функции: '))

    scratch = ScratchCode()

    scratch_code = scratch.generate(serial_number_length, hash_type, hash_length)
    print(f'Скретч-код: {scratch_code}')

    is_right = 'Да' if scratch.check(scratch_code, serial_number_length, hash_type, hash_length) else 'Нет'
    print(f'Правильный? {is_right}')