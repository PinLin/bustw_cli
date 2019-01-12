from .app import App

app = App()


@app.view('init')
def init(data):
    from .init import Init
    return Init(data).main()


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
