from .text import bold

def ask() -> str:
    """接受使用者輸入"""

    while True:
        try:
            select = input(bold("(bustw)> "))
            break

        except KeyboardInterrupt:
            print()

    if select == 'exit':
        raise EOFError

    return select
