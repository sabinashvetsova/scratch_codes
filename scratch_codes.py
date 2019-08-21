from hash import HashCode
from utils import generate_serial_number, get_value


class ScratchCode:
    """Модель скретч-кода"""

    def __init__(self):
        self.key = get_value('key')

    def generate(self, serial_number_length, hash_type, hash_length):
        """
        Генерирует скретч-код.
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :return: Скретч-код
        """

        serial_number = generate_serial_number(serial_number_length)
        input = serial_number + self.key
        hash = HashCode(hash_type)
        hash_string = hash.calc_hash(input)[:hash_length]
        return serial_number + hash_string

    def check(self, user_code, serial_number_length, hash_type, hash_length):
        """
        Проверяет скретч-код.
        :param user_code: Вводимый пользователем скретч-код
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :return: True, если скретч-код верный. False, в обратном случае.
        """

        serial_number = user_code[:serial_number_length]
        input = serial_number + self.key
        hash = HashCode(hash_type)
        hash_string = hash.calc_hash(input)[:hash_length]
        scratch_code = serial_number + hash_string
        return scratch_code == user_code
