import requests


class Bustw:
    def __init__(self):
        self.__base = 'http://localhost:5000'

    def __get(self, resource: str):
        url = self.__base + resource

        return requests.get(url).json()

    def get_info(self, city: str, route: str=''):
        """從伺服器取得路線基本資料"""
        return self.__get(f'/info/{city}/{route}')

    def get_stop(self, city: str, route: str):
        """從伺服器取得路線站牌資料"""
        return self.__get(f'/stop/{city}/{route}')

    def get_real(self, city: str, route: str):
        """從伺服器取得路線定位資料"""
        return self.__get(f'/real/{city}/{route}')

    def get_time(self, city: str, route: str):
        """從伺服器取得路線時間資料"""
        return self.__get(f'/time/{city}/{route}')
