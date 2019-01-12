import requests


class Bustw:
    def __init__(self):
        self.__url = 'https://bus.ntut.com.tw/v1'

    def __fetch(self, url: str, **kwargs):
        url = self.__url + url + '?ver=2'
        url = url.format(**kwargs)

        return requests.get(url).json()

    def get_city(self):
        """從伺服器取得城市資料"""
        return self.__fetch('/city')

    def get_info(self, city: str, route: str=''):
        """從伺服器取得路線基本資料"""
        return self.__fetch('/info/{city}/{route}', city=city, route=route)

    def get_stop(self, city: str, route: str):
        """從伺服器取得路線站牌資料"""
        return self.__fetch('/stop/{city}/{route}', city=city, route=route)

    def get_real(self, city: str, route: str):
        """從伺服器取得路線定位資料"""
        return self.__fetch('/real/{city}/{route}', city=city, route=route)

    def get_time(self, city: str, route: str):
        """從伺服器取得路線時間資料"""
        return self.__fetch('/time/{city}/{route}', city=city, route=route)
