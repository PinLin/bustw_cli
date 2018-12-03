#!/usr/bin/env python3

import sys
from pip._internal import main as pip_main

try:
    with open(sys.path[0] + '/requirements.txt') as f:
        mods = f.read().strip().split('\n')
    list(map(__import__, mods))

except FileNotFoundError:
    pass

except ModuleNotFoundError:
    pip_main(['install', '-r', 'requirements.txt'])

from bustw_cli import app


def main():
    app.run()


if __name__ == '__main__':
    main()
