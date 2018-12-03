from .models import bustw


class App:
    def __init__(self):
        self.__views = {}

    def view(self, func, *args, **kwargs):
        """註冊顯示介面"""

        self.__views[func.__name__] = func

        return func

    def run(self):
        """程式開始執行"""

        # 指定查詢的路線
        choice = self.__views['choose']()
        # 取得資料
        routes = self.__views['call_api'](choice)
        # 顯示結果
        self.__views['display'](choice.split('/')[0], routes)
