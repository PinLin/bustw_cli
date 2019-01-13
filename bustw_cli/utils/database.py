import sys
import sqlite3


class Database:
    def __init__(self):
        self.__db = sqlite3.connect(sys.path[0] + '/bustw_cli/db/bustw.db')

        self.init()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.__db.commit()
        self.__db.close()

    def init(self):
        cursor = self.__db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS city (
            english_name text,
            chinese_name text,
            status integer,
            PRIMARY KEY (english_name)
            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS route (
            routeUID text,
            routeName text,
            city text,
            departureStopName text,
            destinationStopName text,
            FOREIGN KEY (city) REFERENCES city (english_name) ON DELETE CASCADE
            )''')

    def select_city(self) -> list:
        cursor = self.__db.cursor()

        cursor.execute('SELECT * FROM city')
        return cursor.fetchall()

    def insert_city(self, city: dict):
        cursor = self.__db.cursor()

        cursor.execute('INSERT INTO city VALUES (?, ?, ?)',
                       [city['english_name'],
                        city['chinese_name'],
                        city['status']])

    def update_city(self, english_name: str, status: int):
        cursor = self.__db.cursor()

        cursor.execute('UPDATE city SET status=? WHERE english_name=?',
                       (status, english_name))

    def select_route(self, city: str) -> list:
        cursor = self.__db.cursor()

        cursor.execute('SELECT * FROM route WHERE city = ?', [city])
        return cursor.fetchall()

    def insert_route(self, route: dict):
        cursor = self.__db.cursor()

        cursor.execute('INSERT INTO route VALUES (?, ?, ?, ?, ?)',
                       (route['routeUID'],
                        route['routeName'],
                        route['city'],
                        route['departureStopName'],
                        route['destinationStopName：']))

    def delete_routes(self, city: str):
        cursor = self.__db.cursor()

        cursor.execute('DELETE FROM route WHERE city = ?', [city])
