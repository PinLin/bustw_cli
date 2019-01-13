from .base_view import BaseView

import readline

from ..utils.ask import ask
from ..utils.bustw import Bustw
from ..utils.database import Database
from ..utils.text import red, green


class CityView(BaseView):
    def main(self):
        self.data['cities'] = {}    # deprecated
        self.data['routes'] = {}    # deprecated

        with Database() as db:
            if not len(db.select_city()):
                self.download_cities()

        self.load_cities()  # deprecated
        self.select_cities()
        self.download_routes()

        return 'main'

    def download_cities(self):
        """下載城市資料"""

        print("🌐 正在下載城市清單...")
        cities = Bustw().get_city()['cities']

        with Database() as db:
            for city in cities:
                db.insert_city({
                    'english_name': city['key'],
                    'chinese_name': city['name'],
                    'status': 0,
                })

    def load_cities(self):
        """[deprecated] 讀取城市資料"""

        cities = self.data['cities']

        with Database() as db:
            items = db.select_city()

        for item in items:
            cities[item[0]] = {
                'name': item[1],
                'show': item[1] + ('　' if len(item[1]) < 4 else ''),
                'enable': item[2],
            }

    def select_cities(self):
        """選擇要搜尋的資料"""

        cities = self.data['cities']

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

        cities = self.data['cities']
        routes = self.data['routes']

        print()
        for city in cities:
            if not cities[city]['enable']:
                continue

            print("正在下載{city}的路線基本資料...".format(city=cities[city]['name']))
            routes[city] = Bustw().get_info(city)['routes']
