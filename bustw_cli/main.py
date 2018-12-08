from .utils.bustw import Bustw

bustw = Bustw()


class Main:
    def __init__(self, data: dict):
        self.__data = data

    def search(self):
        """設定要搜尋的路線"""

        choice = self.__data['choice']

        if len(choice) < 1 or not choice[0]:
            print()
            print("直接按下 Enter 以進入設定頁")
            print("或是輸入想要查詢的路線（範例：Taipei/72、680、幹線）")

            select = input(self.__data['prompt'])
            try:
                choice[0] = select
            except IndexError:
                choice.append(select)

    def main(self):
        self.search()

        if self.__data['choice'][0] == '':
            return 'setting'

        if self.__data['choice'][0] == 'old':
            return 'old'

        return 'lookup'
