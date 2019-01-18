import sys

from .views.base_view import BaseView


class App:
    def __init__(self, config: dict):
        self.__config = config

    def run(self):
        """程式開始執行"""

        # 讀取外部參數
        choice = sys.argv.copy()
        choice.pop(0)

        try:
            init_view = self.__config['init_view']
            init_view().main(choice)

        except EOFError:
            print()
            print("Bye!")

        except KeyboardInterrupt:
            pass
