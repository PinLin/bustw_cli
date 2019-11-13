import readline

from utils.ask import ask
from utils.city_name import CityName
from utils.database import Database
from views.base_view import BaseView
from views.city_view import CityView
from views.lookup_view import LookupView
from views.setting_view import SettingView


class MainView(BaseView):
    def main(self, choice: list):
        with Database() as db:
            if not len(db.select_city()):
                CityView().main()

        while True:
            if len(choice) < 1 or not choice[0]:
                select = self.search()

                try:
                    choice[0] = select
                except IndexError:
                    choice.append(select)

            if not choice[0]:
                SettingView().main()

                continue

            LookupView().main(choice)

            choice[0] = None

    def search(self):
        """設定要搜尋的路線"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        def completer(text, state):
            commands = city_name.english + city_name.chinese
            options = [i for i in commands if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None
        readline.set_completer(completer)

        question = "🔍 請輸入想要查詢的路線或是按下 Enter 進入設定頁面\n"
        question += "  （範例：72、Keelung.501、台北市.幹線）"
        print()
        answer = ask(question)

        return answer
