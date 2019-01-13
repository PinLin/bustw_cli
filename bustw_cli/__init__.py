from .app import App

app = App()


@app.view('init')
def init(data):
    from .views.init_view import InitView
    return InitView(data).main()


@app.view('city')
def city(data):
    from .city import City
    return City(data).main()


@app.view('main')
def main(data):
    from .main import Main
    return Main(data).main()


@app.view('setting')
def setting(data):
    from .setting import Setting
    return Setting(data).main()


@app.view('lookup')
def lookup(data):
    from .lookup import Lookup
    return Lookup(data).main()


@app.view('result')
def result(data):
    from .result import Result
    return Result(data).main()
