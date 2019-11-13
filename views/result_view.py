from utils.city_name import CityName
from utils.database import Database
from utils.less import print_by_less
from views.base_view import BaseView


class ResultView(BaseView):
    def main(self, info: dict, result: dict):
        self.display(self.process(info, result))

    def process(self, info: dict, result: dict):
        """將取得的資訊整合"""

        uid = info['uid']
        stops = info['stops']
        reals = info['reals']
        times = info['times']

        for sub_route in stops['subRoutes']:
            if sub_route['subRouteUID'] == uid:
                subRouteName = sub_route['subRouteName']
                lastStopName = sub_route['stops'][-1]['stopName']
                result['name'] = subRouteName + "（往" + lastStopName + "）"
                result['stops'] = sub_route['stops'].copy()

        temp = {}
        for time in times:
            if time['routeName'] != result['route_name']:
                continue
            temp[time['stopUID']] = time
        times = temp

        temp = {}
        for real in reals:
            if real['routeName'] != result['route_name']:
                continue
            if not temp.get(real['stopUID']):
                temp[real['stopUID']] = []
            temp[real['stopUID']].append({
                'arriving': real['arriving'],
                'busNumber': real['busNumber'],
                'busStatus': real['busStatus'],
            })
        reals = temp

        for stop in result['stops']:
            time = times[stop['stopUID']]
            stop['estimateTime'] = time['estimateTime']
            stop['stopStatus'] = time['stopStatus']

            real = reals.get(stop['stopUID']) or []
            stop['buses'] = real

        return result

    def title(self, width: int, city: str, route_name: str):
        result = '\033[0;1m［{0}］{1}\033[0m'.format(city, route_name)
        return result.center(width - 6, ' ')

    def display(self, info: dict):
        """顯示查詢結果"""

        width = 52

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        chinese_city_name = city_name.to_chinese(info['city'])

        result = self.title(width, chinese_city_name, info['name'])
        result += "\n"
        result += "—" * width
        result += "\n"

        for stop in info['stops']:
            result += "  "

            # 未發車
            if stop['stopStatus'] == 1:
                result += "\033[47m\033[30m｜ 未發車 ｜\033[0m "

            # 交管不停
            elif stop['stopStatus'] == 2:
                result += "\033[43m\033[30m｜交管不停｜\033[0m "

            # 末班駛離
            elif stop['stopStatus'] == 3:
                result += "\033[47m\033[30m｜末班駛離｜\033[0m "

            # 今日不開
            elif stop['stopStatus'] == 4:
                result += "\033[47m\033[30m｜今日不開｜\033[0m "

            # 有車
            else:
                # 有車且進站中
                if len(stop['buses']) > 0 and 1 in list(map(lambda x: x['arriving'], stop['buses'])):
                    result += "\033[41m\033[97m｜ 進站中 ｜\033[0m "

                # 有車還沒進站
                else:
                    minute = stop['estimateTime'] // 60

                    if minute < 0:
                        result += "\033[47m\033[30m｜ 未發車 ｜\033[0m "
                    elif minute > 2:
                        result += '\033[44m\033[97m｜ {0:>3} 分 ｜\033[0m '.format(
                            minute)
                    else:
                        result += '\033[45m\033[97m｜ {0:>3} 分 ｜\033[0m '.format(
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

        print_by_less(result)
