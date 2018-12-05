from .utils.bustw import Bustw

bustw = Bustw()


class Init:
    def __init__(self, data: dict):
        self.__data = data

    def load_cities(self):
        """讀取城市資料"""

        cities = self.__data['cities']

        for item in bustw.get_city():
            cities[item['key']] = {
                'name': item['name'],
                'enable': False,
            }

    def select_cities(self):
        """選擇要搜尋的資料"""

        cities = self.__data['cities']

        while True:
            for index, value in enumerate(cities.values()):
                print('{index}.{space}{city}\t{status}'.format(
                    index=index + 1,
                    space=("  " if index < 9 else " "),
                    city=value['name'],
                    status=("\033[0;32m　檢索\033[0m" if value['enable'] else "\033[0;31m不檢索\033[0m")))

            print("選擇城市以更改檢索狀態，或按下 Enter 繼續")
            try:
                select = int(input("(bustw)? ")) - 1
                key = list(cities.keys())[select]
                cities[key]['enable'] = not cities[key]['enable']
                print("\n" * 10)
            except Exception:
                break

    def download_routes(self):
        """下載"""

        cities = self.__data['cities']
        routes = self.__data['routes']

        for city in cities:
            if not cities[city]['enable']:
                continue

            routes[city] = bustw.get_info(city)

    def main(self):
        self.__data['cities'] = {}
        self.__data['routes'] = {}

        self.load_cities()
        self.select_cities()
        self.download_routes()

        return 'old_choose'
