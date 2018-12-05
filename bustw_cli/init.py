from .utils.bustw import Bustw

bustw = Bustw()


class Init:
    def __init__(self, data: dict):
        self.__data = data

    def load_cities(self):
        """讀取城市資料"""

        for item in bustw.get_city():
            self.__data['cities'][item['key']] = {
                'name': item['name'],
                'enable': True,
            }

    def main(self):
        self.__data['cities'] = {}

        self.load_cities()

        return 'old_choose'
