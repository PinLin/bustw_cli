#!/usr/bin/env python3

import sys

from bustw_cli import Bustw


def main():
    bustw = Bustw('https://bus.ntut.com.tw/v1')

    try:
        # 指定查詢的路線
        choice = bustw.choose() if len(sys.argv) <= 1 else sys.argv[1]
        # 取得資料
        routes = bustw.call_api(choice)
        # 顯示結果
        bustw.display(choice.split('/')[0], routes)

    except EOFError:
        exit(1)


if __name__ == '__main__':
    main()
