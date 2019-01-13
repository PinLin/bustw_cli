from .base_view import BaseView

import readline

from PyInquirer import prompt

from ..utils.ask import ask
from ..utils.bustw import Bustw
from ..utils.database import Database
from ..utils.text import red, green


class CityView(BaseView):
    def main(self):
        self.data['cities'] = {}    # deprecated
        self.data['routes'] = {}    # deprecated

        with Database() as db:
            if not len(db.select_city()):
                self.download_cities()

        self.load_cities()  # deprecated
        self.select_cities()
        self.download_routes()

        return 'main'

    def download_cities(self):
        """下載城市資料"""

        print("🌐 正在下載城市清單...")
        cities = Bustw().get_city()['cities']

        with Database() as db:
            for city in cities:
                db.insert_city({
                    'english_name': city['key'],
                    'chinese_name': city['name'],
                    'status': 0,
                })

    def load_cities(self):
        """[deprecated] 讀取城市資料"""

        cities = self.data['cities']

        with Database() as db:
            items = db.select_city()

        for item in items:
            cities[item[0]] = {
                'name': item[1],
                'show': item[1] + ('　' if len(item[1]) < 4 else ''),
                'enable': item[2],
            }

    def select_cities(self):
        """選擇要搜尋的資料"""

        with Database() as db:
            cities = db.select_city()

        questions = [
            {
                'type': 'checkbox',
                'qmark': '🏙 ',
                'message': '請選擇要檢索的城市\n',
                'name': 'cities',
                'choices': [
                    {
                        'name': city[1],
                        'checked': city[2]
                    } for city in cities
                ]
            }
        ]

        print()
        answer = prompt(questions)
        print(answer)

    def download_routes(self):
        """下載路線基本資料"""

        cities = self.data['cities']
        routes = self.data['routes']

        print()
        for city in cities:
            if not cities[city]['enable']:
                continue

            print("正在下載{city}的路線基本資料...".format(city=cities[city]['name']))
            routes[city] = Bustw().get_info(city)['routes']
