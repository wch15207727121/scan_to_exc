#!/usr/bin/python
# coding:utf-8
# Author:LinAn@123
# 目标tcp端口开放扫描及应用端口banner识别
import nmap
import sys
import time
import xlwt
import requests
import re
import threading
from threading import Thread
from api.scan_api.nmap_api import nmap_port_scan
# from api.excle_api.excle_api import use_excle
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
R = threading.Lock()
book = xlwt.Workbook()  # 创建Excel

header = {
    'method': 'get',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'
}


def web_scan(host_port):
    try:  #  xxx.xxx.xx.xx:80
        matchObj = re.match(r'^(.*?):(.*\d)$', host_port)
        port = matchObj.group(2)
        R.acquire()
        if port == '80' :
            url_http = ('http://' + str(host_port) + '/')
            get_url(host_port, url_http)
        if port == '443' :
            url_https = ('https://' + str(host_port) + '/')
            get_url(host_port, url_https)
        else:  #  ssl
            url_http = ('http://' + str(host_port) + '/')
            url_https = ('https://' + str(host_port) + '/')
            get_url(host_port, url_http)
            get_url(host_port, url_https)
        R.release()
    except KeyError as e:
        pass


def get_url(host_port, url):
    try:
        r = requests.get(url, headers=header, timeout=2, verify=False)
        r.encoding = r.apparent_encoding
        go_to_ex(host_port, url, r.status_code)
    except requests.exceptions.RequestException as e:
        pass


def go_to_ex(host_port, url, status_code):
    msg = []
    matchObj = re.match(r'^(.*?):(.*\d)$', host_port)
    host = matchObj.group(1)
    port = matchObj.group(2)
    msg.append(str(host))
    msg.append(str(port))
    msg.append(url)
    msg.append(status_code)
    data.append(msg)

if __name__ == '__main__':
    time_start = time.time()
    print ('扫描开始')
    data = []
    t10 = []
    # nmap配置   G:\security_tools\company_security_tools\get_title-master\get_title-master\scan_target.txt   -sV
    main_target = 'scan_target.txt'
    port_list = 'T:80,443,8080,8081,9999,4111,321,8282,8443,8442,8889,8802,5000,5530,8089,9022,9043,9046,9082,25,899'
    arguments = '-p {} -T5 -sS -iL {}'.format(port_list, main_target)
    #print (arguments)
    host_port_list = nmap_port_scan(arguments)  #  xxxx.xxx.xxx.xx:80
    for host_port in host_port_list:
        t1 = Thread(target=web_scan(host_port=host_port), args=(host_port))
        t10.append(t1)
        t1.start()
        t1.join()

    print('-------------')
    print('-------------')
    #print(data)
    # print ('data:--------------------' + str(data) )
    sheet = book.add_sheet('sheet1')  # 创建sheet页
    title = ['ip地址', '端口', 'url地址', '状态码'] # 把表头名称放入list里面  xlwt
    # 循环把表头写入
    row = 0
    for t in title:
        sheet.write(0, row, t)
        row += 1

    row = 1  # 从表格的第二行开始写入数据
    # 一行一行的写，一行对应的所有列
    for i in range(len(data)):  # 控制行
        alis = data[i]
        for one in range(len(alis)):  # 控制每一列 20  0-19   10  0-9
            sheet.write((i + 1), one, alis[one])  # rou代表列，col代表行，one写入值

    book.save('./output/本周渗透任务_存活url.xls')
    print('扫描结束')
    time_end = time.time()
    print (time_end - time_start)
