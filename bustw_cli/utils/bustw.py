import requests


class Bustw:
    def __init__(self):
        self.__url = 'https://bus.ntut.com.tw/v1'

    def fetch(self, url: str, **kwargs):
        """從伺服器取得資料"""

        return requests.get(self.__url + url.format(**kwargs)).json()
