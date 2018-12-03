from .models import bustw


class App:
    def __init__(self):
        self.__views = {}

    def view(self, name: str):
        """註冊顯示介面"""

        def decorator(func, *args, **kwargs):
            # 將函式新增至介面 dict 中
            self.__views[name] = func
            return func
        return decorator

    def run(self):
        """程式開始執行"""

        # 指定查詢的路線
        choice = self.__views['old_choose']()
        # 取得資料
        routes = self.__views['old_call_api'](choice)
        # 顯示結果
        self.__views['old_display'](choice.split('/')[0], routes)
