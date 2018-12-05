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

        # 共享資料
        data = {}

        # 功能跳轉
        func = 'init'
        while True:
            func = self.__views[func](data)
