from .utils.bustw import Bustw


class Init:
    def __init__(self, data: dict):
        self.__data = data
        self.__bustw = Bustw()

    def load_cities(self):
        """讀取城市資料"""

        result = {}
        for item in self.__bustw.get_city():
            result[item['key']] = {
                'name': item['name'],
                'enable': True,
            }
        self.__data['cities'] = result

    def main(self):
        self.load_cities()

        return 'old_choose'
