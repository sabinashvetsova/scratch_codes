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
        Если код еще не был активирован, заносит его в базу.
        user_id в таблице при этом проставляется случайный для имитации ввода кода пользователем.

        :param user_codes: Массив проверяемых кодов
        :param serial_number_length: Длина серийного номера
        :param hash_type: Тип хэш-функции
        :param hash_length: Количество знаков, которые возьмутся от результата хэш-функции
        :return: Словарь: ключи - скретч-коды, значения - True, если скретч-код верный. False, в обратном случае.
        """

        checked_codes = {}

        db = Database()
        db.execute("SELECT code FROM activated_codes;")
        activated_codes = db.fetchall()

        for code in user_codes:
            serial_number = code[:serial_number_length]
            input = serial_number + self.key
            hash = HashCode(hash_type)
            hash_string = hash.calc_hash(input)[:hash_length]
            scratch_code = serial_number + hash_string

            if scratch_code == code and code not in activated_codes:
                db.execute("INSERT INTO activated_codes (code, user_id) VALUES (%s, %s);",
                           (code, random.randint(1, 1000)))
                db.commit()
                checked_codes[code] = True

            else:
                checked_codes[code] = False

        return checked_codes

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
