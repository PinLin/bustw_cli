from .models.bustw import Bustw
from .app import App

bustw = Bustw('https://bus.ntut.com.tw/v1')
app = App()


@app.view('old_choose')
def old_choose():
    """讓使用者選擇要顯示的路線"""

    print("想要查詢什麼路線？（範例：Taipei/72）")
    select = input("> ")
    print()
    return select


@app.view('old_call_api')
def old_call_api(select):
    """向伺服器取得資料"""

    city, route = select.split('/')
    return bustw.fetch('/stop/{city}/{route}', city=city, route=route)['routes']


@app.view('old_display')
def old_display(city, route):
    bustw.old_display(city, route)
