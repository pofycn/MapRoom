# -*- coding: utf-8 -*-

"""
查询适合的租房信息
"""
import requests
import json
import time
import csv
import re

baidu_map_place_api_url = "http://api.map.baidu.com/place/v2"
baidu_map_direction_api_url = "http://api.map.baidu.com/direction/v2"
ak = "bIO0SFId2i4DRAQsM3s3NVnv5sll8p7j"
output = "json"
scope = "2"
office_location_name = ""
traffic_time = ""
region = ""

room_result_data = open("RoomData/room_result.txt", "w")
csv_writer = csv.writer(room_result_data, delimiter=',')


# 根据UID查询百度地图API返回地点详细信息
def get_location_details(uid):
    url = baidu_map_place_api_url \
          + "/detail?uid=" + uid \
          + "&&output=" + output \
          + "&&scope=" + scope \
          + "&&ak=" + ak
    r = requests.get(url)
    # print(str(r.text))
    return str(r.text)


# 根据地点及城市名查询地点详情
def query_location_by_name(location_name, region, city_limit):
    # 防止被API限制并发，返回结果正确则直接返回，401则重试
    while True:
        url = baidu_map_place_api_url + "/suggestion?query=" \
              + location_name + "&region=" \
              + region + "&city_limit=" \
              + city_limit + "&output=" \
              + output + "&ak=" + ak
        r = requests.get(url)
        # print(str(r.text))
        result = json.loads(str(r.text))
        # 并发控制，睡眠1s
        if result['status'] == 401:
            print(str(r.text))
            time.sleep(3)
        if len(result['result']) == 0:
            return "0"
        else:
            return str(r.text)


# 根据起点及终点坐标信息获取路线信息
def get_direction_transit(origin_position, destination_position):
    # 并发控制  免费API限制QPS
    while True:
        time.sleep(1)
        url = baidu_map_direction_api_url + "/transit?origin=" \
              + origin_position + "&destination=" \
              + destination_position + "&ak=" + ak
        r = requests.get(url)
        result = json.loads(str(r.text))
        # 并发控制，睡眠1s
        if result['status'] == 401:
            print(str(r.text))
            time.sleep(3)
        # print(str(r.text))
        return str(r.text)


# 获取行程时长及路线的平均时长
def get_duration(direction_result_str):
    direction_result = json.loads(direction_result_str)
    # print(direction_result['result']['routes'])
    sum_time = 0
    plan_count = 0
    for ele in direction_result['result']['routes']:
        # print(ele['duration'])
        sum_time += ele['duration']
        plan_count += 1
    ave_cost_time = format(float(sum_time) / float(plan_count * 60), '.2f')
    # print("average cost time(minutes):", ave_cost_time)
    return ave_cost_time


# 根据地点信息获取周围附近的坐标
def get_position(location_result_str):
    location_result = json.loads(location_result_str)
    latitude = location_result['result'][0]['location']['lat']
    longitude = location_result['result'][0]['location']['lng']
    # print("lat:", latitude, " lng:", longitude)
    return str(latitude) + "," + str(longitude)


# 从文件中读取房源地址
def get_room_address_from_file():
    file = open('RoomData/room_data.csv', 'r')
    result_list = list()
    count_lines = 0
    for line in open('RoomData/room_data.csv'):
        line = file.readline()
        # print(line)
        result_list.append(line)
        count_lines += 1
    file.close()
    # print(result_list)
    return result_list


# 根据房间信息结果找到符合条件的房间信息
def find_my_room(room_info_list):
    des_pos_location_str = query_location_by_name(office_location_name, region, "true")
    des_pos_location = get_position(des_pos_location_str)
    print("destination_position:", des_pos_location)
    result_list = list()
    for room_info in room_info_list:
        print("name:", str(room_info).split(',')[0])
        origin_pos_location_str = query_location_by_name(str(room_info).split(',')[0], region, "true")
        if origin_pos_location_str == "0":
            continue
        origin_pos_location = get_position(origin_pos_location_str)
        # print("origin_pos_location:", origin_pos_location)
        direction_result_str = get_direction_transit(origin_pos_location, des_pos_location)
        # print("direction_result_str", direction_result_str)
        cost_time = get_duration(direction_result_str)

        print("cost time:", cost_time, " minutes")
        if (cost_time <= traffic_time):
            result_list.append(room_info)
            room_result_data.write("公寓名:" + str(room_info).split(',')[0] + "\n" +
                                   "公寓所在区域：" + str(room_info).split(',')[1] + "\n" +
                                   "通勤消耗时间：" + cost_time + "minutes\n" +
                                   "公寓链接：" + str(room_info).split(',')[3] + "\n" +
                                   "----------------------------------------------\n")
            # csv_writer.writerow(
            #     ["公寓名:" + str(room_info).split(',')[0] + "\n",
            #      "公寓所在区域：" + str(room_info).split(',')[1] + "\n",
            #      "通勤消耗时间：" + cost_time + "\n",
            #      "公寓链接：" + str(room_info).split(',')[3] + "\n"])
    # print(result_list)
    return result_list


if __name__ == "__main__":
    print("query house start...")
    # get_location_details(test_uid)

    # location_result_str = query_location_by_name("景田餼龤号公寓", "深圳", "true")
    # print(get_position(location_result_str))

    # direction_result_str = get_direction_transit("40.056878,116.30815", "31.222965,121.505821")
    # print(get_duration(direction_result_str))

    # get_room_address_from_file()

    region = "深圳"
    # region = input("请输入你所在的城市：")
    office_location_name = '百度国际大厦'
    # office_location_name = input("请输入工作地点：")
    traffic_time = "60"
    # traffic_time = input("请输入期望的通勤时间：")

    room_info_list = get_room_address_from_file()
    find_my_room(room_info_list)
    print("查询完成！结果请查看/RoomData下的room_result.txt")
