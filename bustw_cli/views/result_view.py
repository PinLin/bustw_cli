from .base_view import BaseView

import readline

from ..utils.ask import ask
from ..utils.bustw import Bustw
from ..utils.city_name import CityName
from ..utils.database import Database
from ..utils.less import print_less


class ResultView(BaseView):
    def __init__(self, data: dict):
        super().__init__(data)

        self.__stops = None
        self.__reals = None
        self.__times = None
        self.__uid = None
        self.__info = {}

    def main(self):
        self.download_stops()

        while True:
            if not self.choose():
                self.data['choice'] = self.data['choice'][:1]
                break

            self.download_reals()
            self.download_times()

            self.process()
            self.display()

            self.data['choice'] = self.data['choice'][:2]

        # 是否有外部參數
        if len(self.data['args']) < 3:
            return 'lookup'
        else:
            return 'exit'

    def download_stops(self):
        """下載路線站牌資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("正在下載{0}之路線 {1} 的站牌資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_stop(result['city'], result['routeName'])['routes']

        for route in data:
            if route['routeUID'] == result['routeUID']:
                self.__stops = route
                return

    def download_reals(self):
        """下載路線定位資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("正在下載{0}之路線 {1} 的定位資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_real(result['city'], result['routeName'])['buses']

        temp = []
        for route in data:
            if route['routeUID'] == result['routeUID']:
                temp.append(route)
        self.__reals = temp

    def download_times(self):
        """下載路線時間資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("正在下載{0}之路線 {1} 的時間資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_time(result['city'], result['routeName'])['stops']

        temp = []
        for route in data:
            if route['routeUID'] == result['routeUID']:
                temp.append(route)
        self.__times = temp

    def choose(self):
        """選擇要查詢的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        choice = self.data['choice']
        result = self.data['result']
        stops = self.__stops

        while True:
            texts = []
            if len(choice) < 3 or not choice[2]:
                print()
                print("以下是{0}之路線 {1} 的子路線".format(
                    city_name.to_chinese(result['city']),
                    result['routeName']))

                print()
                for index, value in enumerate(stops['subRoutes']):
                    subRouteName = value['subRouteName']
                    lastStopName = value['stops'][-1]['stopName']

                    texts.append(subRouteName + "（往" + lastStopName + "）")

                    print('{0:<3} {1}'.format(
                        str(index + 1) + ".",
                        subRouteName + "（往" + lastStopName + "）"))

                print()
                print("選擇想要查詢的子路線")

                def completer(text, state):
                    commands = texts
                    options = [i for i in commands if i.startswith(text)]
                    if state < len(options):
                        return options[state]
                    else:
                        return None

                readline.set_completer(completer)
                try:
                    select = ask()
                except KeyboardInterrupt:
                    print()
                    return False

                try:
                    choice[2] = select
                except IndexError:
                    choice.append(select)

            try:
                index = int(choice[2]) - 1
                self.__uid = stops['subRoutes'][index]['subRouteUID']
                return True

            except ValueError:
                if choice[2] in texts:
                    index = texts.index(choice[2])
                    self.__uid = stops['subRoutes'][index]['subRouteUID']
                    return True

                print()
                print("沒有找到任何路線，請重新查詢。")
                choice.pop(2)

            except IndexError:
                choice.pop(2)

    def process(self):
        info = self.__info

        info['city'] = self.data['result']['city']

        for sub_route in self.__stops['subRoutes']:
            if sub_route['subRouteUID'] == self.__uid:
                subRouteName = sub_route['subRouteName']
                lastStopName = sub_route['stops'][-1]['stopName']
                info['name'] = subRouteName + "（往" + lastStopName + "）"
                info['stops'] = sub_route['stops'].copy()

        temp = {}
        for time in self.__times:
            if time['routeName'] != self.data['result']['routeName']:
                continue
            temp[time['stopUID']] = time
        self.__times = temp

        temp = {}
        for real in self.__reals:
            if real['routeName'] != self.data['result']['routeName']:
                continue
            if not temp.get(real['stopUID']):
                temp[real['stopUID']] = []
            temp[real['stopUID']].append({
                'arriving': real['arriving'],
                'busNumber': real['busNumber'],
                'busStatus': real['busStatus'],
            })
        self.__reals = temp

        for stop in info['stops']:
            time = self.__times[stop['stopUID']]
            stop['estimateTime'] = time['estimateTime']
            stop['stopStatus'] = time['stopStatus']

            real = self.__reals.get(stop['stopUID']) or []
            stop['buses'] = real

    def display(self):

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        info = self.__info

        result = ''
        result += '\n'
        result += '{0} {1}'.format(city_name.to_chinese(info['city']), info['name'])
        result += '\n'
        result += "=" * 50
        result += '\n'

        for stop in info['stops']:
            # 未發車
            if stop['stopStatus'] == 1:
                result += "\033[47m\033[30m[ 未發車 ]\033[0m "

            # 交管不停
            elif stop['stopStatus'] == 2:
                result += "\033[43m\033[30m[交管不停]\033[0m "

            # 末班駛離
            elif stop['stopStatus'] == 3:
                result += "\033[47m\033[30m[末班駛離]\033[0m "

            # 今日不開
            elif stop['stopStatus'] == 4:
                result += "\033[47m\033[30m[今日不開]\033[0m "

            # 有車
            else:
                # 有車且進站中
                if len(stop['buses']) > 0 and 1 in list(map(lambda x: x['arriving'], stop['buses'])):
                    result += "\033[41m\033[97m[ 進站中 ]\033[0m "

                # 有車還沒進站
                else:
                    minute = stop['estimateTime'] // 60

                    if minute > 2:
                        result += '\033[44m\033[97m[ {0:>3} 分 ]\033[0m '.format(
                            minute)
                    else:
                        result += '\033[45m\033[97m[ {0:>3} 分 ]\033[0m '.format(
                            minute)

            # 分析站名有多寬
            length = 0
            for char in stop['stopName']:
                length += 2 if ord(char) > 127 else 1
            # 顯示公車站名稱（最多 30 字）
            result += stop['stopName'][:30] + ' ' * (30 - length)

            # 如果有車的話顯示車號
            if len(stop['buses']) > 0:
                for bus in stop['buses']:
                    # 有多台車就換行
                    if stop['buses'].index(bus) != 0:
                        result += " " * 41
                    result += bus['busNumber']
                    result += '\n'
            else:
                result += '\n'

        print_less(result)
