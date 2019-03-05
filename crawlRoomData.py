# -*- coding: utf-8 -*-

"""
crawlRoomData
~~~~~~~~~~~~
抓取58页面上的公寓租房信息
"""

from bs4 import BeautifulSoup
import requests
import csv
import time

# 为了方便主要抓取价格3000~5000 面积大小10~30平的房子 且为整租的方案 如需特殊的定制需求可以更改URL对应的参数
shenzhen_room_info_url = "https://sz.58.com/pinpaigongyu/pn/{page}/?minprice=3000_5000&area=10_30&fangshi=1"

# 完成抓取的页面数据的页码
page = 0
csv_file = open("RoomData/room_data.csv", "w")
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", shenzhen_room_info_url.format(page=page))
    # 判断有反爬机制 每次抓取页面sleep 1s
    time.sleep(1)
    response = requests.get(shenzhen_room_info_url.format(page=page))
    html = BeautifulSoup(response.text, features="html.parser")
    room_list = html.select(".list > li")
    # 读取不到房源，结束
    if not room_list:
        break

    for room in room_list:
        title = room.select("h2")[0].string
        room_url = room.select("a")[0]["href"]
        room_info_list = title.split()
        s = str(title).lstrip().rstrip()
        title_list = s.split(" ")
        room_title = (title_list[0] + title_list[1]).split("】")[1]

        # 如果第二列是公寓名则取第一列作为地址
        if "公寓" in room_info_list[1] or "青年社区" in room_info_list[1]:
            location = room_info_list[0]
        else:
            location = room_info_list[1]
        price = room.select(".money")[0].select("b")[0].string
        # 价格以及房型做了反爬处理，暂时留空
        csv_writer.writerow([room_title, location, "", room_url])

csv_file.close()
