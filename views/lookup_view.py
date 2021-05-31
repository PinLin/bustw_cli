from PyInquirer import prompt

from utils.city import City
from utils.database import Database
from views.base_view import BaseView
from views.switch_view import SwitchView


class LookupView(BaseView):
    def main(self, choice: list):
        routes = self.select_routes(choice[0])
        if len(routes) == 0:
            print()
            print("🚌 沒有找到任何路線，請再試一次。")

            return

        while True:
            if len(choice) < 2 or not choice[1]:
                select = self.choose(routes)

                try:
                    choice[1] = select
                except IndexError:
                    choice.append(select)

            if not choice[1]:
                choice[1] = None

                return

            choice[1] = int(choice[1]) - 1

            result = routes[choice[1]]

            SwitchView().main(choice, result)

            choice[1] = None

    def select_routes(self, route_name: str):
        """取得資料庫中名稱符合的路線"""

        with Database() as db:
            routes = db.select_route(route_name)

        return routes

    def choose(self, routes: list):
        """選擇要查詢的路線"""

        choices = list(map(lambda x: '［{0}］{1}'.format(
            City().translate(x['city']), x['route_name']), routes))

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
