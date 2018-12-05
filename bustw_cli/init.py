from .utils.bustw import Bustw

bustw = Bustw()


def load_cities():
    """讀取城市資料"""

    result = {}
    for item in bustw.get_city():
        result[item['key']] = {
            'name': item['name'],
            'enable': True,
        }
    return result


def main(data: dict):
    data['cities'] = load_cities()

    return 'old_choose'
