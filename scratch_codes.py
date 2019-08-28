import random

from hash import HashCode
from utils import get_value
from db import Database


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
        Проверяет скретч-коды в 2 этапа:
        1) Сначала вычисляет серийный номер переданного кода. Склеивает его с секретным ключом.
        Вычисляет хэш от результата и берет определенное кол-во символов от получившейся строки.
        Склеивает серийный номер с получившейся строкой. Полученный скретч-код сравнивает с переданным.
        2) Если коды совпадают, то проверяет есть ли такой код в базе активированных кодов.

        :param user_codes: Массив проверяемых кодов
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :returns: tuple (checked_codes, right_codes)
            - checked_codes: Словарь. Ключи - скретч-коды, значения: True, если код верный, False - в обратном случае
            - right_codes: Массив с правильными кодами
        """

        checked_codes = {}
        right_codes = []
        activated_codes = self.get_activated_codes()

        for code in user_codes:
            serial_number = code[:serial_number_length]
            input = serial_number + self.key
            hash = HashCode(hash_type)
            hash_string = hash.calc_hash(input)[:hash_length]
            scratch_code = serial_number + hash_string

            if scratch_code == code and code not in activated_codes:
                checked_codes[code] = True
                right_codes.append(code)

            else:
                checked_codes[code] = False

        return checked_codes, right_codes

    @staticmethod
    def create_activated_codes_table():
        """
        Создает таблицу с активированными кодами, если ее не существует.
        """

        db = Database()
        db.execute("""CREATE TABLE IF NOT EXISTS activated_codes(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(255) NOT NULL,
            activation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_id INT NOT NULL);""")

    @staticmethod
    def get_activated_codes():
        """
        Получает все активированные коды из таблицы.
        """

        db = Database()
        db.execute("SELECT code FROM activated_codes;")
        return [code[0] for code in db.fetchall()]

    @staticmethod
    def add_new_codes(codes):
        """
        Заносит правильные до этого момента не активированные коды в базу.
        user_id в таблице при этом проставляется случайный для имитации ввода кода пользователем.
        :param codes: Массив правильных кодов
        """

        records = []
        insert_query = "INSERT INTO activated_codes (code, user_id) VALUES (%s, %s);"
        db = Database()

        for code in codes:
            records.append((code, random.randint(1, 1000)))

        db.executemany(insert_query, records)
        db.commit()
