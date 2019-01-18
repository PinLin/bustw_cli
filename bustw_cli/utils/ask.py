import readline


def ask(text: str='') -> str:
    """接受使用者輸入"""

    readline.parse_and_bind("tab: complete")

    if text:
        print('\033[0;1m{}\033[0m'.format(text))
    select = input(' ❯ ')

    if select == 'exit':
        raise EOFError

    return select
