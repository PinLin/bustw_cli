from .utils.bustw import Bustw

bustw = Bustw()


class Lookup:
    def __init__(self, data: dict):
        self.__data = data
        self.__picked = []

    def filter(self):
        """篩選出符合條件的路線"""

        routes = self.__data['routes']
        choice = self.__data['choice']
        picked = self.__picked

        temp = []
        for route in list(routes.values()):
            temp += route

        for route in temp:
            if choice[0] in route['routeName']:
                picked.append(route)

    def choose(self):
        """選擇要查詢的路線"""

        cities = self.__data['cities']
        choice = self.__data['choice']
        picked = self.__picked

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

        self.__data['result'] = picked[int(choice[1]) - 1]

    def main(self):
        self.filter()
        self.choose()

        # TODO: 移除此區塊
        self.__data['choice'] = []
        return 'main'
