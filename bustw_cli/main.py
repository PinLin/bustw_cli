import readline

from .utils.ask import ask
from .utils.bustw import Bustw

bustw = Bustw()


class Main:
    def __init__(self, data: dict):
        self.__data = data

    def search(self):
        """設定要搜尋的路線"""

        cities = self.__data['cities']
        choice = self.__data['choice']

        if len(choice) < 1 or not choice[0]:
            print()
            print("直接按下 Enter 以進入設定頁")
            print("或是輸入想要查詢的路線（範例：Taipei.72、680、台北市.幹線）")

            def completer(text, state):
                commands = cities.keys()
                options = [i for i in commands if i.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None

            readline.set_completer(completer)
            select = ask()

            try:
                choice[0] = select
            except IndexError:
                choice.append(select)

    def main(self):
        self.search()

        if self.__data['choice'][0] == '':
            return 'setting'

        return 'lookup'
