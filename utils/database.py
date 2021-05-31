import sys
import sqlite3


class Database:
    def __init__(self):
        self.__db = sqlite3.connect(sys.path[0] + '/data.db')

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
            route_uid text,
            route_name text,
            city text,
            departure_stop_name text,
            destination_stop_name text,
            FOREIGN KEY (city) REFERENCES city (english_name) ON DELETE CASCADE
            )''')

    def select_city(self) -> list:
        cursor = self.__db.cursor()

        cursor.execute('SELECT * FROM city')

        def to_dict(data: list) -> dict:
            return {
                'english_name': data[0],
                'chinese_name': data[1],
                'status': data[2],
            }
        return list(map(to_dict, cursor.fetchall()))

    def insert_city(self, city: dict):
        cursor = self.__db.cursor()

        cursor.execute('INSERT INTO city VALUES (?, ?, ?)',
                       [city['english_name'],
                        city['chinese_name'],
                        city['status']])

    def update_city(self, english_name: str, status: int):
        cursor = self.__db.cursor()

        cursor.execute('UPDATE city SET status=? WHERE english_name=?',
                       [status, english_name])

    def select_route(self, route_name: str) -> list:
        cursor = self.__db.cursor()

        cursor.execute('SELECT * FROM route WHERE route_name LIKE ?',
                       ['%' + route_name + '%'])

        def to_dict(data: list) -> dict:
            return {
                'route_uid': data[0],
                'route_name': data[1],
                'city': data[2],
                'departure_stop_name': data[3],
                'destination_stop_name': data[4],
            }
        return list(map(to_dict, cursor.fetchall()))

    def insert_route(self, route: dict):
        cursor = self.__db.cursor()

        cursor.execute('INSERT INTO route VALUES (?, ?, ?, ?, ?)',
                       [route['route_uid'],
                        route['route_name'],
                        route['city'],
                        route['departure_stop_name'],
                        route['destination_stop_name']])

    def delete_routes(self, city: str):
        cursor = self.__db.cursor()

        cursor.execute('DELETE FROM route WHERE city = ?', [city])
