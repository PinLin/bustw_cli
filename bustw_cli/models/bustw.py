import requests


class Bustw:
    def __init__(self, url: str):
        self.__url = url

    def fetch(self, url: str, **kwargs):
        """從伺服器取得資料"""

        return requests.get(self.__url + url.format(**kwargs)).json()

    def old_display(self, city, routes):
        """選擇查看的路線"""

        select = 0
        if len(routes) > 1:
            # 提示訊息
            print("哪一個才是您想要的路線？")
            # 顯示查詢到的所有路線
            for route in routes:
                print("{0}. {1}".format(routes.index(
                    route) + 1, route['routeName']))
            print()
            # 接收使用者的輸入
            select = int(input("> ")) - 1
            # 輸入完畢
            print()

        # 使用者想要查看的路線的子路線們
        subRoutes = routes[select]['subRoutes']

        # 選擇查看的子路線
        select = 0
        if len(subRoutes) > 1:
            # 提示訊息
            print("哪一個子路線？")
            # 顯示查詢到的所有路線
            for subRoute in subRoutes:
                print("{0}. {1}".format(subRoutes.index(
                    subRoute) + 1, subRoute['subRouteName']))
            print()
            # 接收使用者的輸入
            select = int(input("> ")) - 1
            # 輸入完畢
            print()
        # 使用者想要查看的路線
        subRoute = subRoutes[select]

        # 顯示路線名稱
        print("（{0}）{1}".format(city, subRoute['subRouteName']))
        print("{0} <-> {1}".format(subRoute['stops'][0]
                                   ['stopName'], subRoute['stops'][-1]['stopName']))
        # 顯示公車站與車子位置
        print("===================================================")
        for stop in subRoute['stops']:
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
                    minute, _ = divmod(stop['estimateTime'], 60)
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
