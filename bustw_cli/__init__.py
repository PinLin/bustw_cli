from .models.bustw import Bustw
from .app import App

bustw = Bustw('https://bus.ntut.com.tw/v1')
app = App()


@app.view('choose')
def choose():
    return bustw.choose()


@app.view('call_api')
def call_api(select):
    return bustw.call_api(select)


@app.view('display')
def display(city, route):
    bustw.display(city, route)
