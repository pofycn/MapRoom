# -*- coding: utf-8 -*-
"""
CrawRoomData单元测试
"""
import unittest
import requests

shenzhen_room_info_url = "https://sz.58.com/pinpaigongyu/pn/{page}/?minprice=3000_5000&area=10_30&fangshi=1"


class TestCrawlRoomData(unittest.TestCase):
    def test_connection(self):
        """
        测试接口连通性
        :return:
        """
        request_result = requests.get(shenzhen_room_info_url.format(page=1))
        self.assertEqual(200, request_result.status_code)


if __name__ == '__main__':
    unittest.main()
