from .utils.bustw import Bustw

bustw = Bustw()


class Lookup:
    def __init__(self, data: dict):
        self.__data = data

    def main(self):
        # TODO: 移除此區塊
        self.__data['choice'] = []
        return 'main'
