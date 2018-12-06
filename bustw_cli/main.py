from .utils.bustw import Bustw

bustw = Bustw()


class Main:
    def __init__(self, data: dict):
        self.__data = data

    def choose(self):
        args = self.__data['args']

        print()
        print("直接按下 Enter 以進入設定頁")
        print("或是輸入想要查詢的路線（範例：72、680、幹線）")
        args.append(input(self.__data['prompt']))

    def main(self):
        self.choose()

        if self.__data['args'][0] == '':
            return 'setting'

        return 'lookup'
