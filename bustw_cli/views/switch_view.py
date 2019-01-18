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
        choice = self.data['choice']

        stops = self.download_stops()

        if len(choice) < 3 or not choice[2]:
            result = self.choose(stops)

            try:
                choice[2] = result
            except IndexError:
                choice.append(result)

        if not choice[2]:
            choice[2] = None
            choice[1] = None

            return 'lookup'

        choice[2] = int(choice[2]) - 1

        self.__uid = stops['subRoutes'][choice[2]]['subRouteUID']

        reals = self.download_reals()
        times = self.download_times()

        self.process(stops, reals, times)

        return 'result'

    def download_stops(self):
        """下載路線站牌資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = self.data['result']

        print()
        print("🌐 正在下載{0}之路線 {1} 的站牌資料...".format(
            city_name.to_chinese(result['city']),
            result['route_name']))
        data = Bustw().get_stop(result['city'], result['route_name'])['routes']

        for route in data:
            if route['routeUID'] == result['route_uid']:
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
            result['route_name']))
        data = Bustw().get_real(result['city'], result['route_name'])['buses']

        temp = []
        for route in data:
            if route['routeUID'] == result['route_uid']:
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
            result['route_name']))
        data = Bustw().get_time(result['city'], result['route_name'])['stops']

        temp = []
        for route in data:
            if route['routeUID'] == result['route_uid']:
                temp.append(route)
        return temp

    def choose(self, stops: dict):
        """選擇要查詢的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

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
                    result['route_name']),
                'choices': choices
            }
        ]

        print()
        try:
            answer = prompt(questions)['answer']
        except KeyError:
            raise KeyboardInterrupt
        print()

        return choices.index(answer)

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
            if time['routeName'] != self.data['result']['route_name']:
                continue
            temp[time['stopUID']] = time
        times = temp

        temp = {}
        for real in reals:
            if real['routeName'] != self.data['result']['route_name']:
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
