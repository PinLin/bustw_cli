from .base_view import BaseView

from ..utils.database import Database


class InitView(BaseView):
    """初始化"""

    def main(self):
        with Database() as db:
            # 判斷縣市及路線資料是否已下載
            if len(db.select_city()):
                return 'main'

            else:
                return 'city'
