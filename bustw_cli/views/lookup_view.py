from .base_view import BaseView

from PyInquirer import prompt

from ..utils.city_name import CityName
from ..utils.database import Database


class LookupView(BaseView):
    def main(self):
        if self.choose():
            return 'result'

        self.data['choice'] = []
        return 'main'

    def choose(self):
        """選擇要查詢的路線"""

        choice = self.data['choice']

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

            routes = db.select_route(choice[0])

        if len(routes) == 0:
            print()
            print("🚌 沒有找到任何路線，請再試一次。")

            self.data['result'] = None
            return False

        choices = list(map(lambda x: '［{0}］{1}'.format(
            city_name.to_chinese(x[2]), x[1]), routes))

        questions = [
            {
                'type': 'list',
                'qmark': '🚌 ',
                'name': 'choice',
                'message': '請選擇要查看的路線\n',
                'choices': choices
            }
        ]

        if len(choice) < 2 or not choice[1]:
            print()
            answer = prompt(questions)['choice']
            print()

            try:
                choice[1] = choices.index(answer)
            except IndexError:
                choice.append(choices.index(answer))

            route = routes[choice[1]]
            self.data['result'] = {
                'routeUID': route[0],               # TODO: Rename
                'routeName': route[1],              # TODO: Rename
                'city': route[2],                   # TODO: Rename
                'departureStopName': route[3],      # TODO: Rename
                'destinationStopName': route[4],    # TODO: Rename
            }

        return True
