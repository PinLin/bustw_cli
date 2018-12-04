import requests


class Bustw:
    def __init__(self):
        self.__url = 'https://bus.ntut.com.tw/v1'

    def __fetch(self, url: str, ver: int, **kwargs):
        url = self.__url + url + '?ver={ver}'.format(ver=ver) if ver else ''
        url = url.format(**kwargs)

        return requests.get(url).json()

    def get_city(self, city: str='', ver: int=None):
        """從伺服器取得城市資料"""
        return self.__fetch('/city/{city}', ver, city=city)

    def get_info(self, city: str, route: str='', ver: int=None):
        """從伺服器取得路線基本資料"""
        return self.__fetch('/info/{city}/{route}', ver, city=city, route=route)

    def get_stop(self, city: str, route: str='', ver: int=None):
        """從伺服器取得路線站牌資料"""
        return self.__fetch('/stop/{city}/{route}', ver, city=city, route=route)

    def get_real(self, city: str, route: str='', ver: int=None):
        """從伺服器取得路線定位資料"""
        return self.__fetch('/real/{city}/{route}', ver, city=city, route=route)

    def get_time(self, city: str, route: str='', ver: int=None):
        """從伺服器取得路線時間資料"""
        return self.__fetch('/time/{city}/{route}', ver, city=city, route=route)

    def fetch(self, url: str, **kwargs):
        """從伺服器取得資料"""

        return requests.get(self.__url + url.format(**kwargs)).json()
