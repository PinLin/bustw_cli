from .models.bustw import Bustw
from .app import App

bustw = Bustw('https://bus.ntut.com.tw/v1')
app = App()


@app.view('old_choose')
def old_choose():
    """讓使用者選擇要顯示的路線"""

    # 提示訊息
    print("想要查詢什麼路線？（範例：Taipei/72）")
    # 接收使用者的輸入
    select = input("> ")
    # 輸入完畢
    print()
    # 回傳路線名稱
    return select


@app.view('old_call_api')
def old_call_api(select):
    return bustw.old_call_api(select)


@app.view('old_display')
def old_display(city, route):
    bustw.old_display(city, route)
