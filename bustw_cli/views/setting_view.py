from .base_view import BaseView

from PyInquirer import prompt


class SettingView(BaseView):
    def main(self):
        return self.select_function()

    def select_function(self):
        functions = {
            '回到主畫面': 'main',
            '修改要檢索的城市': 'city',
        }

        questions = [
            {
                'type': 'list',
                'qmark': '🔧 ',
                'name': 'choice',
                'message': '請選擇要修改的設定\n',
                'choices': functions.keys()
            }
        ]

        print()
        answer = prompt(questions)['choice']
        print()

        return functions[answer]
