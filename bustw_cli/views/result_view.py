from .base_view import BaseView

from ..utils.city_name import CityName
from ..utils.database import Database
from ..utils.less import print_less


class ResultView(BaseView):
    def main(self):
        self.display(self.data['info'])

        self.data['choice'] = self.data['choice'][:2]

        return 'switch'

    def display(self, info):
        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        result = '\033[0;1m［{0}］{1}\033[0m\n'.format(
            city_name.to_chinese(info['city']), info['name'])
        result += "=" * 50 + '\n'

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
