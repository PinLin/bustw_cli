from .app import App

app = App()


@app.view('init')
def init(data):
    from .views.init_view import InitView
    return InitView(data).main()


@app.view('city')
def city(data):
    from .views.city_view import CityView
    return CityView(data).main()


@app.view('main')
def main(data):
    from .views.main_view import MainView
    return MainView(data).main()


@app.view('setting')
def setting(data):
    from .views.setting_view import SettingView
    return SettingView(data).main()


@app.view('lookup')
def lookup(data):
    from .lookup import Lookup
    return Lookup(data).main()


@app.view('result')
def result(data):
    from .result import Result
    return Result(data).main()
