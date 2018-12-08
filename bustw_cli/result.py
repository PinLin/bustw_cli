import readline

from .utils.ask import ask
from .utils.bustw import Bustw

bustw = Bustw()


class Result:
    def __init__(self, data: dict):
        self.__data = data

    def main(self):
        # TODO: 示意
        print("Success!")

        # 沒有外部參數
        if len(self.__data['args']) < 2:
            self.__data['choice'] = []
            return 'main'

        # 有外部參數
        else:
            return 'exit'
