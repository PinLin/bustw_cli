from PyInquirer import prompt

from utils.bustw import Bustw
from utils.city_name import CityName
from utils.database import Database
from views.base_view import BaseView


class CityView(BaseView):
    def main(self):
        with Database() as db:
            if not len(db.select_city()):
                self.download_cities()

        self.select_cities()
        self.update_routes()

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

    def select_cities(self):
        """選擇要搜尋的資料"""

        with Database() as db:
            cities = db.select_city()
            city_name = CityName(cities)

        questions = [
            {
                'type': 'checkbox',
                'qmark': '🏙 ',
                'message': '請選擇要檢索的城市\n',
                'name': 'answer',
                'choices': [
                    {
                        'name': city['chinese_name'],
                        'checked': city['status']
                    } for city in cities
                ]
            }
        ]

        print()
        try:
            answer = prompt(questions)['answer']
        except KeyError:
            raise KeyboardInterrupt
        print()

        with Database() as db:
            for chinese_name in city_name.chinese:
                english_name = city_name.to_english(chinese_name)
                db.update_city(english_name, chinese_name in answer)

    def update_routes(self):
        """更新路線基本資料"""

        with Database() as db:
            cities = db.select_city()

        for city in cities:
            if city['status']:
                print("🌐 正在下載{city}的路線基本資料...".format(
                    city=city['chinese_name']))
                routes = Bustw().get_info(city['english_name'])['routes']
                with Database() as db:
                    db.delete_routes(city['english_name'])

                    for route in routes:
                        db.insert_route({
                            'route_uid': route['routeUID'],
                            'route_name': route['routeName'],
                            'city': route['city'],
                            'departure_stop_name': route['departureStopName'],
                            'destination_stop_name': route['destinationStopName'],
                        })

            else:
                with Database() as db:
                    db.delete_routes(city['english_name'])
