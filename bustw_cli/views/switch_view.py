from .base_view import BaseView

from PyInquirer import prompt

from ..utils.bustw import Bustw
from ..utils.city_name import CityName
from ..utils.database import Database


class SwitchView(BaseView):
    def __init__(self, data: dict):
        super().__init__(data)

        self.__uid = None

    def main(self):
        stops = self.download_stops()

        if self.choose(stops):
            reals = self.download_reals()
            times = self.download_times()

            self.process(stops, reals, times)
            return 'result'

        self.data['choice'] = self.data['choice'][:1]

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
        print("🌐 正在下載{0}之路線 {1} 的站牌資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_stop(result['city'], result['routeName'])['routes']

        for route in data:
            if route['routeUID'] == result['routeUID']:
                return route

    def download_reals(self):
        """下載路線定位資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("🌐 正在下載{0}之路線 {1} 的定位資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_real(result['city'], result['routeName'])['buses']

        temp = []
        for route in data:
            if route['routeUID'] == result['routeUID']:
                temp.append(route)
        return temp

    def download_times(self):
        """下載路線時間資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("🌐 正在下載{0}之路線 {1} 的時間資料...".format(
            city_name.to_chinese(result['city']),
            result['routeName']))
        data = Bustw().get_time(result['city'], result['routeName'])['stops']

        temp = []
        for route in data:
            if route['routeUID'] == result['routeUID']:
                temp.append(route)
        return temp

    def choose(self, stops):
        """選擇要查詢的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        choice = self.data['choice']
        result = self.data['result']

        choices = list(map(lambda x: '{0}（往{1}）'.format(
            x['subRouteName'], x['stops'][-1]['stopName']), stops['subRoutes']))

        choices.insert(0, '  回到主畫面')

        questions = [
            {
                'type': 'list',
                'qmark': '🛣 ',
                'name': 'answer',
                'message': '請選擇要查看的［{0}］{1} 之子路線\n'.format(
                    city_name.to_chinese(result['city']),
                    result['routeName']),
                'choices': choices
            }
        ]

        if len(choice) < 3 or not choice[2]:
            print()
            try:
                answer = prompt(questions)['answer']
            except KeyError:
                raise KeyboardInterrupt
            print()

            if answer == '  回到主畫面':
                self.data['result'] = None
                return False

            try:
                choice[2] = choices.index(answer)
            except IndexError:
                choice.append(choices.index(answer))

        index = int(choice[2]) - 1
        self.__uid = stops['subRoutes'][index]['subRouteUID']
        return True

    def process(self, stops, reals, times):
        self.data['info'] = {}
        info = self.data['info']

        info['city'] = self.data['result']['city']

        for sub_route in stops['subRoutes']:
            if sub_route['subRouteUID'] == self.__uid:
                subRouteName = sub_route['subRouteName']
                lastStopName = sub_route['stops'][-1]['stopName']
                info['name'] = subRouteName + "（往" + lastStopName + "）"
                info['stops'] = sub_route['stops'].copy()

        temp = {}
        for time in times:
            if time['routeName'] != self.data['result']['routeName']:
                continue
            temp[time['stopUID']] = time
        times = temp

        temp = {}
        for real in reals:
            if real['routeName'] != self.data['result']['routeName']:
                continue
            if not temp.get(real['stopUID']):
                temp[real['stopUID']] = []
            temp[real['stopUID']].append({
                'arriving': real['arriving'],
                'busNumber': real['busNumber'],
                'busStatus': real['busStatus'],
            })
        reals = temp

        for stop in info['stops']:
            time = times[stop['stopUID']]
            stop['estimateTime'] = time['estimateTime']
            stop['stopStatus'] = time['stopStatus']

            real = reals.get(stop['stopUID']) or []
            stop['buses'] = real
