from .models.bustw import Bustw
from .app import App

bustw = Bustw('https://bus.ntut.com.tw/v1')
app = App()


@app.view
def choose():
    return bustw.choose()


@app.view
def call_api(select):
    return bustw.call_api(select)


@app.view
def display(city, route):
    bustw.display(city, route)
