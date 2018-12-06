from .utils.bustw import Bustw

bustw = Bustw()


class Old:
    def __init__(self, data: dict):
        self.__data = data

    def main(self):
        print()
        print("請輸入要搜尋的「城市/路線」（例如：Taipei/72）。")

        city_name, route_name = input("> ").split('/')
        routes = bustw.get_stop(city_name, route_name)['routes']

        if len(routes) > 1:
            print()

            # 印出候選路線
            for route in routes:
                print("{0}. {1}".format(routes.index(
                    route) + 1, route['routeName']))

            print()
            print("請選擇想要查看的路線。")

            select = int(input("> ")) - 1

        else:
            select = 0

        sub_routes = routes[select]['subRoutes']

        if len(sub_routes) > 1:

            print()

            # 印出候選子路線
            for sub_route in sub_routes:
                print("{0}. {1}".format(sub_routes.index(
                    sub_route) + 1, sub_route['subRouteName']))

            print()
            print("請選擇想要查看的子路線。")

            select = int(input("> ")) - 1

        else:
            select = 0

        sub_route = sub_routes[select]

        # 顯示路線資訊
        print()
        print("（{0}）{1}".format(city_name, sub_route['subRouteName']))
        print("{0} <-> {1}".format(sub_route['stops'][0]['stopName'],
                                   sub_route['stops'][-1]['stopName']))
        print("===================================================")

        for stop in sub_route['stops']:
            # 未發車
            if stop['stopStatus'] == 1:
                print("\033[47m\033[30m[ 未發車 ]\033[0m ", end='')

            # 交管不停
            elif stop['stopStatus'] == 2:
                print("\033[43m\033[30m[交管不停]\033[0m ", end='')

            # 末班駛離
            elif stop['stopStatus'] == 3:
                print("\033[47m\033[30m[末班駛離]\033[0m ", end='')

            # 今日不開
            elif stop['stopStatus'] == 4:
                print("\033[47m\033[30m[今日不開]\033[0m ", end='')

            # 有車
            else:
                # 有車且進站中
                if len(stop['buses']) > 0 and 1 in list(map(lambda x: x['arriving'], stop['buses'])):
                    print("\033[41m\033[97m[ 進站中 ]\033[0m ", end='')

                # 有車還沒進站
                else:
                    minute = stop['estimateTime'] // 60

                    if minute > 2:
                        print("\033[44m\033[97m[ {0: >3} 分 ]\033[0m ".format(
                            minute), end='')
                    else:
                        print("\033[45m\033[97m[ {0: >3} 分 ]\033[0m ".format(
                            minute), end='')

            # 分析站名有多寬
            length = 0
            for char in stop['stopName']:
                length += 2 if ord(char) > 127 else 1
            # 顯示公車站名稱（最多 30 字）
            print(stop['stopName'][:30] + ' ' * (30 - length), end='')

            # 如果有車的話顯示車號
            if len(stop['buses']) > 0:
                for bus in stop['buses']:
                    # 有多台車就換行
                    if stop['buses'].index(bus) != 0:
                        print(" " * 41, end='')
                    print(bus['busNumber'])
            else:
                print()

        return 'exit'
