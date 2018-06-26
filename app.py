#!/usr/bin/env python3

import sys
import json
import requests

# 讓使用者選擇要顯示的路線
def choose(choices):
    # 提示訊息
    print("想要查詢什麼路線？（範例：Taipei/72）")
    # 顯示可查詢的路線
    for choice in choices:
        print("{0}. {1}".format(choices.index(choice) + 1, choice))
    print()
    # 接收使用者的輸入
    select = input("> ")
    # 輸入完畢
    print()
    try:
        # 如果輸入清單序號就回傳路線名稱
        return choices[int(select) - 1]
    except ValueError:
        # 回傳路線名稱
        return select
    

# 向伺服器取得資料
def call_api(select):
    # 向伺服器發出請求
    response = requests.get("https://bus.ntut.com.tw/v1/stop/" + select)
    # 回傳所有路線資料
    return json.loads(response.text)['routes']

def display(city, routes):
    # 選擇查看的路線
    select = 0
    if len(routes) > 1:
        # 提示訊息
        print("哪一個才是您想要的路線？")
        # 顯示查詢到的所有路線
        for route in routes:
            print("{0}. {1}".format(routes.index(route) + 1, route['routeName']))
        print()
        # 接收使用者的輸入
        select = int(input("> ")) - 1
        # 輸入完畢
        print()
    
    # 使用者想要查看的路線的子路線們
    subRoutes = routes[select]['subRoutes']

    # 選擇查看的子路線
    select = 0
    if len(subRoutes) > 1:
        # 提示訊息
        print("哪一個子路線？")
        # 顯示查詢到的所有路線
        for subRoute in subRoutes:
            print("{0}. {1}".format(subRoutes.index(subRoute) + 1, subRoute['subRouteName']))
        print()
        # 接收使用者的輸入
        select = int(input("> ")) - 1
        # 輸入完畢
        print()
    # 使用者想要查看的路線
    subRoute = subRoutes[select]

    # 顯示路線名稱
    print("（{0}）{1}".format(city, subRoute['subRouteName']))
    print("{0} <-> {1}".format(subRoute['stops'][0]['stopName'], subRoute['stops'][-1]['stopName']))
    # 顯示公車站與車子位置
    print("===================================================")
    for stop in subRoute['stops']:
        # 未發車
        if stop['stopStatus'] == 1:
            print("[ 未發車 ] ", end='')
        # 交管不停
        elif stop['stopStatus'] == 2:
            print("[交管不停] ", end='')
        # 末班駛離
        elif stop['stopStatus'] == 3:
            print("[末班駛離] ", end='')
        # 今日不開
        elif stop['stopStatus'] == 4:
            print("[今日不開] ", end='')
        # 有車
        else:
            # 有車且進站中
            if len(stop['buses']) > 0 and 1 in list(map(lambda x: x['arriving'], stop['buses'])):
                print("[ 進站中 ] ", end='')
            # 有車還沒進站
            else:
                minute, _ = divmod(stop['estimateTime'], 60)
                print("[ {0: >3} 分 ] ".format(minute), end='')
        # 分析站名有多寬
        length = 0
        for char in stop['stopName']:
            length += 2 if ord(char) > 127 else 1
        # 顯示公車站名稱
        print(stop['stopName'] + ' ' * (30 -length), end='')
        # 如果有車的話顯示車號
        if len(stop['buses']) > 0:
            for bus in stop['buses']:
                print(bus['busNumber'], end=' ')
            print()
        else:
            print()

def help():
    print("bustw - 一個 CLI 的查公車工具\n"
          "用法：\n"
          "\n"
          "bustw [<City>/<RouteName>]  - 查詢公車\n"
          "bustw -h, --help            - 顯示此幫助\n")

def main():
    # 引數
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        help()
        exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        help()
        exit(0)
    
    # 曾經查詢過的路線
    try:
        f = open(sys.path[0] + '/history.json', 'r')
        choices = json.load(f)
        f.close()
    except FileNotFoundError:
        choices = []

    try:
        # 指定查詢的路線
        choice = choose(choices) if len(sys.argv) <= 1 else sys.argv[1]
        # 取得資料
        routes = call_api(choice)
        # 顯示結果
        display(choice.split('/')[0], routes)
    except EOFError:
        exit(1)

    # 將路線名稱就加入清單內
    choices.append(choice)
    # 去除重複
    history = sorted(set(choices), key=choices.index)
    # 儲存到曾經查詢的路線中
    f = open(sys.path[0] + '/history.json', 'w')
    json.dump(history, f, ensure_ascii=False, indent=4)
    f.close()

if __name__ == '__main__':
    main()
