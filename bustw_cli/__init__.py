from .models.bustw import Bustw
from .app import App

bustw = Bustw('https://bus.ntut.com.tw/v1')
app = App()


@app.view('old_choose')
def old_choose():
    return bustw.old_choose()


@app.view('old_call_api')
def old_call_api(select):
    return bustw.old_call_api(select)


@app.view('old_display')
def old_display(city, route):
    bustw.old_display(city, route)
