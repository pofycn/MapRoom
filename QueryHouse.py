# -*- coding: utf-8 -*-

"""
查询适合的租房信息
"""
import requests

baidu_map_detail_url = "http://api.map.baidu.com/place/v2/detail?"
ak = "ImVgRmw8SH96Vz58c05d43BO0TvSgkFV"
uid = ""
output = "json"
scope = "2"


def getLocationDetail():
    # http://api.map.baidu.com/place/v2/detail?uid=435d7aea036e54355abbbcc8&output=json&scope=2&ak=您的密钥 //GET请求
    url = baidu_map_detail_url + "uid=435d7aea036e54355abbbcc8&&output=" + output + "&&scope=" + scope + "&&ak=" + ak
    r = requests.get(url)
    print(str(r.text))


if __name__ == "__main__":
    getLocationDetail()
