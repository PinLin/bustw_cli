import readline

from .utils.ask import ask
from .utils.bustw import Bustw

bustw = Bustw()


class Result:
    def __init__(self, data: dict):
        self.__data = data
        self.__uid = None
        self.__stops = None

    def download_stops(self):
        """下載路線站牌資料"""

        cities = self.__data['cities']
        result = self.__data['result']

        print()
        print("正在下載{0}之路線 {1} 的站牌資料...".format(
            cities[result['city']]['name'],
            result['routeName']))
        data = bustw.get_stop(result['city'], result['routeName'], 2)

        for route in data:
            if route['routeUID'] == result['routeUID']:
                self.__stops = route
                return

    def choose(self):
        """選擇要查詢的路線"""

        cities = self.__data['cities']
        choice = self.__data['choice']
        result = self.__data['result']
        stops = self.__stops

        while True:
            texts = []
            if len(choice) < 3 or not choice[2]:
                print()
                print("以下是{0}之路線 {1} 的子路線".format(
                    cities[result['city']]['name'],
                    result['routeName']))

                print()
                for index, value in enumerate(stops['subRoutes']):
                    subRouteName = value['subRouteName']
                    lastStopName = value['stops'][-1]['stopName']

                    texts.append(subRouteName + "（往" + lastStopName + "）")

                    print('{0:<3} {1}'.format(
                        str(index + 1) + ".",
                        subRouteName + "（往" + lastStopName + "）"))

                print()
                print("選擇想要查詢的子路線")

                def completer(text, state):
                    commands = texts
                    options = [i for i in commands if i.startswith(text)]
                    if state < len(options):
                        return options[state]
                    else:
                        return None

                readline.set_completer(completer)
                try:
                    select = ask()
                except KeyboardInterrupt:
                    print()
                    return False

                try:
                    choice[2] = select
                except IndexError:
                    choice.append(select)

            try:
                index = int(choice[2]) - 1
                self.__uid = stops['subRoutes'][index]['subRouteUID']
                return True

            except ValueError:
                if choice[2] in texts:
                    index = texts.index(choice[2])
                    self.__uid = stops['subRoutes'][index]['subRouteUID']
                    return True

                print()
                print("沒有找到任何路線，請重新查詢。")
                choice.pop(2)

            except IndexError:
                choice.pop(2)

    def main(self):
        self.download_stops()

        while True:
            if not self.choose():
                self.__data['choice'] = self.__data['choice'][:1]
                break

            # TODO: 示意
            print("Success!")
            self.__data['choice'] = self.__data['choice'][:2]

        # 是否有外部參數
        if len(self.__data['args']) < 3:
            return 'lookup'
        else:
            return 'exit'
