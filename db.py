import mysql.connector
import random
import sys


class Database(object):
    """ Модель базы данных. """

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(user='user', password='pass',
                                           host='127.0.0.1',
                                           database='scratch_codes')

            self.cursor = self.conn.cursor()

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS activated_codes(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(255) NOT NULL,
            activation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_id INT NOT NULL);""")

        except mysql.connector.errors.ProgrammingError:
            print('Что-то пошло не так при соединении с базой')
            sys.exit()

    def check_codes(self, codes):
        """
        Проверяет, были ли коды уже активированы до этого, и если не были, заносит в базу.
        :param codes: Массив кодов
        :return: Словарь: ключи - скретч-коды, значения - True, если скретч-код не был активирован. False, в обратном случае.
        """

        for code, is_right in codes.items():
            if is_right:
                self.cursor.execute("SELECT * FROM activated_codes WHERE code = %s;", (code,))

                activated_code = self.cursor.fetchone()

                if activated_code:
                    codes[code] = False

                else:
                    self.cursor.execute("INSERT INTO activated_codes (code, user_id) VALUES (%s, %s);",
                                        (code, random.randint(1, 1000)))
                    self.conn.commit()

        return codes
