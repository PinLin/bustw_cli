import readline

from .utils.ask import ask
from .utils.bustw import Bustw
from .utils.text import red, green

bustw = Bustw()


class City:
    def __init__(self, data: dict):
        self.__data = data

    def load_cities(self):
        """讀取城市資料"""

        cities = self.__data['cities']

        print("正在下載城市清單...")
        items = bustw.get_city()['cities']
        for item in items:
            cities[item['key']] = {
                'name': item['name'],
                'show': item['name'] + ('　' if len(item['name']) < 4 else ''),
                'enable': (item['key'] in [
                    # 預設檢索
                    'Keelung', 'Taipei', 'NewTaipei', 'InterCity'
                ]),
            }

    def select_cities(self):
        """選擇要搜尋的資料"""

        cities = self.__data['cities']

        print()
        while True:
            print("\n" * 20)

            for index, couple in enumerate(cities.items()):
                key, value = couple
                print('{0:<3} {1:^5} {2:^10}'.format(
                    str(index + 1) + ".",
                    value['show'],
                    green(" 檢索") if value['enable'] else red("不檢索")))

            print()
            print("選擇城市以更改檢索狀態，或直接按下 Enter 以繼續")

            def completer(text, state):
                commands = cities.keys()
                options = [i for i in commands if i.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None

            readline.set_completer(completer)
            while True:
                try:
                    select = ask()
                    break
                except KeyboardInterrupt:
                    print()

            if select == '':
                break
            try:
                # 使用者輸入數字
                key = list(cities.keys())[int(select) - 1]
                cities[key]['enable'] = not cities[key]['enable']

            except ValueError:
                # 使用者輸入字串
                key = select
                if key in cities:
                    cities[key]['enable'] = not cities[key]['enable']

            except EOFError as e:
                raise e

            except Exception:
                continue

    def download_routes(self):
        """下載路線基本資料"""

        cities = self.__data['cities']
        routes = self.__data['routes']

        print()
        for city in cities:
            if not cities[city]['enable']:
                continue

            print("正在下載{city}的路線基本資料...".format(city=cities[city]['name']))
            routes[city] = bustw.get_info(city)['routes']

    def main(self):
        self.__data['cities'] = {}
        self.__data['routes'] = {}

        self.load_cities()
        self.select_cities()
        self.download_routes()

        return 'main'
