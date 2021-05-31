import requests


class Bustw:
    def __init__(self):
        self.__base = 'http://localhost:5000'

    def __get(self, resource: str, **kwargs):
        url = self.__base + resource + '?ver=3'
        url = url.format(**kwargs)

        return requests.get(url).json()

    def get_info(self, city: str, route: str=''):
        """從伺服器取得路線基本資料"""
        return self.__get('/info/{city}/{route}', city=city, route=route)

    def get_stop(self, city: str, route: str):
        """從伺服器取得路線站牌資料"""
        return self.__get('/stop/{city}/{route}', city=city, route=route)

    def get_real(self, city: str, route: str):
        """從伺服器取得路線定位資料"""
        return self.__get('/real/{city}/{route}', city=city, route=route)

    def get_time(self, city: str, route: str):
        """從伺服器取得路線時間資料"""
        return self.__get('/time/{city}/{route}', city=city, route=route)
