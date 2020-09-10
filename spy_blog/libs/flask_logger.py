__author__ = 'SPing'
import json
import time
import sys
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import g, Response, request, _request_ctx_stack
from models.blog import User



def register_logger(name):
    APP_LOG_FP = 'logs/app.log'
    logger = logging.getLogger(name)
    dir_name, _ = os.path.split(APP_LOG_FP)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    logger.setLevel(logging.INFO)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)-2s[%(name)s]: %(message)s')
    # 文件日志
    file_handler = RotatingFileHandler(APP_LOG_FP, maxBytes=10 * 1024 * 1024, backupCount=7)
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    # logger.setLevel(logging.DEBUG)
    return logger


REG_XP = r'[{](.*?)[}]'
OBJECTS = ['user', 'response', 'request']


# 记录每次请求的性能
def apply_request_log(app):
    @app.before_request
    def request_cost_time():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

    @app.after_request
    def log_response(res):
        message = '[%s] -> [%s] from:%s costs:%.3f ms' % (
            request.method,
            request.path,
            request.remote_addr,
            float(g.request_time()) * 1000
        )
        req_body = request.get_json() if request.get_json() else {}
        data = {
            'path': request.path,
            'query': request.args,
            'body': req_body
        }
        message += '\n\"data\": ' + json.dumps(data, indent=4, ensure_ascii=False)
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            print(message)
        return res


# # 记录用户的登录日志
# def record_login_log(uid: str):
#     '''
#     :param uid: 用户id
#     :return:
#     '''
#     remote_addr, user_agent = request.remote_addr, request.user_agent
#     location = parse_location_by_ip(ip=remote_addr)
#     user = User.query.get(uid)
#     if user:
#         user.update({
#             'login_ip': remote_addr,
#             'login_addr': location
#         })
#         user.commit_to_db()


import geoip2.database

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
# reader = geoip2.database.Reader(
#     '../data/GeoLite2-City.mmdb')


# def ip_print_AddrInfo(ip):
#     # Replace "city" with pthe method corresponding to the database
#     # that you are using, e.g., "country".
#     # -----------------------------------------------
#     # 载入指定IP相关数据
#     response = reader.city(ip)
#     # 读取国家代码
#     Country_IsoCode = response.country.iso_code
#     # 读取国家名称
#     Country_Name = response.country.name
#     # 读取国家名称(中文显示)
#     Country_NameCN = response.country.names['zh-CN']
#     # 读取州(国外)/省(国内)名称
#     Country_SpecificName = response.subdivisions.most_specific.name
#     # 读取州(国外)/省(国内)代码
#     Country_SpecificIsoCode = response.subdivisions.most_specific.iso_code
#     # 读取城市名称
#     City_Name = response.city.name
#     # 读取邮政编码
#     City_PostalCode = response.postal.code
#     # 获取纬度
#     Location_Latitude = response.location.latitude
#     # 获取经度
#     Location_Longitude = response.location.longitude
#     # ------------------------------------------------打印
#     print('[*] Target: ' + ip + ' GeoLite2-Located ')
#     if Country_IsoCode != None:
#         print('  [+] Country_IsoCode        : ' + Country_IsoCode)
#     if Country_Name:
#         print('  [+] Country_Name           : ' + Country_Name)
#     if Country_NameCN != None:
#         print('  [+] Country_NameCN         : ' + Country_NameCN)
#     if Country_SpecificName != None:
#         print('  [+] Country_SpecificName   : ' + Country_SpecificName)
#     if Country_SpecificIsoCode != None:
#         print('  [+] Country_SpecificIsoCode: ' + Country_SpecificIsoCode)
#     if City_Name != None:
#         print('  [+] City_Name              : ' + City_Name)
#     if City_PostalCode != None:
#         print('  [+] City_PostalCode        : ' + City_PostalCode)
#     if Location_Latitude != None:
#         print('  [+] Location_Latitude      : ' + str(Location_Latitude))
#     if Location_Longitude != None:
#         print('  [+] Location_Longitude     : ' + str(Location_Longitude))
#
#
#
# # 基于ip解析真实地址
# def parse_location_by_ip(ip: str):
#     '''
#     :param ip: ip地址
#     :return: ip所在的省市
#     '''
#     if ip == '127.0.0.1' or ip.startswith('192.168.'):
#         return "本地"
#     from common.http_util import HTTP
#     try:
#         url = 'http://whois.pconline.com.cn/ipJson.jsp?{0}&json=true'.format(ip)
#         json_data = HTTP.get(url)
#         return '{0} {1}'.format(json_data['pro'], json_data['city'])
#     except Exception:
#         return '获取地理位置异常 {ip}'.format(ip=ip)
#
#
# if __name__ == '__main__':
#     print(parse_location_by_ip('192.168.0.1'))
#     import socket
#     hostname = socket.gethostname()
#     host = socket.gethostbyname(hostname)
#     print(host)
#     ip_print_AddrInfo('39.97.220.46')