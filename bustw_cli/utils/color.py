def red(text: str) -> str:
    return '\033[0;31m{}\033[0m'.format(text)


def green(text: str) -> str:
    return '\033[0;32m{}\033[0m'.format(text)
