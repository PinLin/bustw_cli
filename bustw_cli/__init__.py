from .app import App
from .views.main_view import MainView

app = App({
    'init_view': MainView,
})
