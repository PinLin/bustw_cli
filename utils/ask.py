import readline


def ask(text: str = '') -> str:
    """接受使用者輸入"""

    readline.parse_and_bind("tab: complete")

    if text:
        print(f'\033[0;1m{text}\033[0m')

    try:
        select = input(' ❯ ')

    except KeyboardInterrupt as e:
        print()
        print()
        print("Cancelled by user")
        print()

        raise e

    if select == 'exit':
        raise EOFError

    return select
