from hash import HashCode
from utils import get_value


class ScratchCode:
    """Модель скретч-кода"""

    def __init__(self):
        self.key = get_value('key')


    def generate(self, serial_number_length, hash_type, hash_length, scratch_codes_count):
        """
        Генерирует скретч-коды.
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :param scratch_codes_count: Количество скретч-кодов
        :return: Скретч-код
        """

        scratch_codes = []
        serial_number = get_value('first_serial_number').zfill(serial_number_length)

        for _ in range(scratch_codes_count):
            input = serial_number + self.key
            hash = HashCode(hash_type)
            hash_string = hash.calc_hash(input)[:hash_length]
            scratch_codes.append(serial_number + hash_string)
            serial_number = str(int(serial_number) + 1).zfill(serial_number_length)

        return scratch_codes


    def check(self, user_codes, serial_number_length, hash_type, hash_length):
        """
        Проверяет скретч-коды.
        :param user_codes: Массив проверяемых кодов
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :return: Словарь: ключи - скретч-коды, значения - True, если скретч-код верный. False, в обратном случае.
        """

        checked_codes = {}

        for code in user_codes:
            serial_number = code[:serial_number_length]
            input = serial_number + self.key
            hash = HashCode(hash_type)
            hash_string = hash.calc_hash(input)[:hash_length]
            scratch_code = serial_number + hash_string
            checked_codes[code] = scratch_code == code

        return checked_codes
