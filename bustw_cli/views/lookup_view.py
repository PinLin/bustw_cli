from .base_view import BaseView

from PyInquirer import prompt

from ..utils.city_name import CityName
from ..utils.database import Database


class LookupView(BaseView):
    def main(self):
        choice = self.data['choice']

        routes = self.select_routes(choice[0])
        if len(routes) == 0:
            print()
            print("🚌 沒有找到任何路線，請再試一次。")

            return 'main'

        if len(choice) < 2 or not choice[1]:
            select = self.choose(routes)

            try:
                choice[1] = select
            except IndexError:
                choice.append(select)

        if not choice[1]:
            choice[1] = None
            choice[0] = None

            return 'main'

        choice[1] = int(choice[1]) - 1

        self.data['result'] = routes[choice[1]]

        return 'switch'

    def select_routes(self, route_name: str):
        """取得資料庫中名稱符合的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

            if '.' in route_name:
                city, select = route_name.split('.')

                if city in city_name.chinese:
                    city = city_name.to_english(city)

                routes = db.select_route(select, city)

            else:
                routes = db.select_route(route_name)

        return routes

    def choose(self, routes: list):
        """選擇要查詢的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        choices = list(map(lambda x: '［{0}］{1}'.format(
            city_name.to_chinese(x['city']), x['route_name']), routes))

        choices.insert(0, '  回到主畫面')

        questions = [
            {
                'type': 'list',
                'qmark': '🚌 ',
                'name': 'answer',
                'message': '請選擇要查看的路線\n',
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
