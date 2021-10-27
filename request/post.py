# coding: utf-8
# !/bin/python

import urllib
import urllib2
import json


# TODO 推送至预警api
def warning_request(message, metric):
    print('post warning request {}: {}'.format(message, metric))


# url = 'http://httpbin.org/post'
# url = 'http://127.0.0.1:5000/sys_check'
#
# payload = {'name': 'wujimaster'}
# header = {'Content-Type': 'application/json'}
#
# data = json.dumps(payload)
# request = urllib2.Request(url, data=data, headers=header)
# response = urllib2.urlopen(url=request, timeout=15)
#
# result = response.read()
#
# print(result)

# 请求字段格式
# {
# 	"message": "",
# 	"host": "",
# 	"resource": "",
# }
