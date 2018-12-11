from .text import bold


def ask() -> str:
    """接受使用者輸入"""

    select = input(bold("(bustw)> "))

    if select == 'exit':
        raise EOFError

    return select
