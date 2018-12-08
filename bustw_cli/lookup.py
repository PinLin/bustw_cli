from .utils.bustw import Bustw

bustw = Bustw()


class Lookup:
    def __init__(self, data: dict):
        self.__data = data
        self.__picked = []

    def filter(self):
        """篩選出符合條件的路線"""

        cities = self.__data['cities']
        routes = self.__data['routes']
        choice = self.__data['choice']
        picked = self.__picked

        # 合併所有縣市的路線
        temp = []
        for route in list(routes.values()):
            temp += route

        # 篩選符合條件的路線
        for route in temp:
            if not choice[0].split('/')[-1] in route['routeName']:
                continue
            if '/' in choice[0]:
                if choice[0].split('/')[0] != route['city']:
                    if choice[0].split('/')[0] != cities[route['city']]['name']:
                        continue
            picked.append(route)

    def choose(self):
        """選擇要查詢的路線"""

        cities = self.__data['cities']
        choice = self.__data['choice']
        picked = self.__picked

        if len(picked) == 0:
            print()
            print("沒有找到任何路線，請重新查詢。")

            self.__data['result'] = None
            return False

        while True:
            if len(choice) < 2 or not choice[1]:
                print()
                for index, value in enumerate(picked):
                    print('{index}.{space}{city}\t{route}'.format(
                        index=index + 1,
                        space=("  " if index < 9 else " "),
                        city=cities[value['city']]['name'],
                        route=value['routeName']))

                print()
                print("選擇想要查詢的路線")

                select = input(self.__data['prompt'])
                try:
                    choice[1] = select
                except IndexError:
                    choice.append(select)

            try:
                self.__data['result'] = picked[int(choice[1]) - 1]
                return True

            except IndexError:
                choice.pop(1)

    def main(self):
        self.filter()
        if self.choose():
            print("Success!")

            # TODO: 移除此區塊
            self.__data['choice'] = []
            return 'main'

        else:
            self.__data['choice'] = []
            return 'main'
