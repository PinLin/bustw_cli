from utils.ask import ask
from utils.database import Database
from views.base_view import BaseView
from views.city_view import CityView
from views.lookup_view import LookupView
from views.setting_view import SettingView


class MainView(BaseView):
    def main(self):
        with Database() as db:
            if not len(db.select_city()):
                CityView().main()

        choice = []
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

        question = "🔍 請輸入想要查詢的路線或是按下 Enter 進入設定頁面\n"
        question += "  （範例：72、501、幹線）"
        print()
        answer = ask(question)

        return answer
