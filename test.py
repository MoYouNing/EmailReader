import requests
import json
import time

# url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
# r = requests.get(url)
# data = json.loads(r.text).get('data')['t']
# ticks = time.time()
# print(ticks)
# data = list(data)
# data[10] = '.'
# data = ''.join(data)
#
# lt = time.localtime(float(data))
if __name__ == '__main__':
    url = 'http://x.xx1.1x1.xx0:10000/mail/'
    data = {"imageId": "xxxx", "base64Data": "xxxx", "format": "jpg", "url": "xxxxx"}
    data = json.dumps(data)
    r = requests.post(url)

    print(json.loads(r.text).get('From'))




# print(time.localtime().)
# def is_chinese(string):
#     """
#     检查整个字符串是否包含中文
#     :param string: 需要检查的字符串
#     :return: bool
#     """
#     for ch in string:
#         if u'\u4e00' <= ch <= u'\u9fff':
#             return True
#
#     return False
#
# ret1 = is_chinese("chinese")
# print(ret1)
#
# ret2 = is_chinese("12亦3")
# print(ret2)
