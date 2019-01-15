from .base_view import BaseView

import readline

from ..utils.ask import ask
from ..utils.city_name import CityName
from ..utils.database import Database


class MainView(BaseView):
    def main(self):
        self.search()

        if self.data['choice'][0] == '':
            return 'setting'

        return 'lookup'

    def search(self):
        """設定要搜尋的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        choice = self.data['choice']

        if len(choice) < 1 or not choice[0]:
            def completer(text, state):
                commands = city_name.english + city_name.chinese
                options = [i for i in commands if i.startswith(text)]
                if state < len(options):
                    return options[state]
                else:
                    return None

            readline.set_completer(completer)
            print()
            select = ask(
                "🔍 請輸入想要查詢的路線或是按下 Enter 進入設定頁面\n  （範例：72、Keelung.501、台北市.幹線）")

            try:
                choice[0] = select
            except IndexError:
                choice.append(select)
