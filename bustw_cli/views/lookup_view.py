from .base_view import BaseView

from PyInquirer import prompt

from ..utils.city_name import CityName
from ..utils.database import Database


class LookupView(BaseView):
    def main(self):
        if self.choose():
            return 'switch'

        self.data['choice'] = []
        return 'main'

    def choose(self):
        """選擇要查詢的路線"""

        choice = self.data['choice']

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

            if '.' in choice[0]:
                city, select = choice[0].split('.')
                
                if city in city_name.chinese:
                    city = city_name.to_english(city)

                routes = db.select_route(select, city)
            else:
                routes = db.select_route(choice[0])

        if len(routes) == 0:
            print()
            print("🚌 沒有找到任何路線，請再試一次。")

            self.data['result'] = None
            return False

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

        if len(choice) < 2 or not choice[1]:
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
                choice[1] = choices.index(answer)
            except IndexError:
                choice.append(choices.index(answer))

        index = int(choice[1]) - 1
        route = routes[index]
        self.data['result'] = route

        return True
