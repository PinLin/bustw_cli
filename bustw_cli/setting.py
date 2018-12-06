from .utils.bustw import Bustw

bustw = Bustw()


class Setting:
    def __init__(self, data: dict):
        self.__data = data

    def main(self):
        return 'main'
