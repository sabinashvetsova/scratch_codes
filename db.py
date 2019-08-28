import mysql.connector
import sys

from utils import get_value


class Database(object):
    """ Модель базы данных. """

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(user=get_value('db_user'),
                                                password=get_value('db_password'),
                                                host=get_value('db_host'),
                                                database=get_value('db_name'))

            self.cursor = self.conn.cursor()

        except mysql.connector.errors.ProgrammingError:
            print('Что-то пошло не так при соединении с базой')
            sys.exit()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)

    def executemany(self, query, records):
        self.cursor.executemany(query, records)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()
