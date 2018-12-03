import requests


class Bustw:
    def __init__(self, url: str):
        self.__url = url

    def fetch(self, url: str, **kwargs):
        """從伺服器取得資料"""

        return requests.get(self.__url + url.format(**kwargs)).json()
