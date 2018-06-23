#!/usr/bin/env python3

from pprint import pprint
import json
import requests

# 讓使用者選擇要顯示的路線
def choose():
    # 可查詢的路線
    choices = [
        "Taipei/72",
        "Taipei/680",
        "Taipei/212夜",
        "NewTaipei/953去",
        "NewTaipei/953返",
        "NewTaipei/953區",
        "InterCity/1815",
    ]
    # 提示訊息
    print("想要查詢什麼路線？")
    # 顯示可查詢的路線
    for choice in choices:
        print("{0}. {1}".format(choices.index(choice) + 1, choice))
    print("\n（輸入序號或手動輸入其他路線）")
    # 接收使用者的輸入
    select = input("> ")
    # 輸入完畢
    print()
    try:
        return choices[int(select) - 1]
    except ValueError:
        return select
    

# 向伺服器取得資料
def call_api(select):
    # 向伺服器發出請求
    response = requests.get("https://bus.ntut.com.tw/v1/stop/" + select)
    # 回傳所有路線資料
    return json.loads(response.text)['routes']

def display(routes):
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
            print("{0}. {1}（往{2}）".format(subRoutes.index(subRoute) + 1, subRoute['subRouteName'], subRoute['stops'][-1]['stopName']))
        print()
        # 接收使用者的輸入
        select = int(input("> ")) - 1
        # 輸入完畢
        print()
    # 使用者想要查看的路線
    subRoute = subRoutes[select]

    # 顯示路線名稱
    print("{0}".format(subRoute['subRouteName']))
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


def main():
    choice = choose()
    routes = call_api(choice)
    display(routes)

if __name__ == '__main__':
    main()