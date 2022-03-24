import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse
import urllib.parse
# 获取日志logger
import logging

logger = logging.getLogger(__name__)


class LogMiddle(MiddlewareMixin):
    # 日志处理中间件
    def process_request(self, request):
        # 存放请求过来时的时间
        request.init_time = time.time()
        path = request.path
        if path.endswith('jsi18n/'):
            return HttpResponse()
        # print(request.user)
        # logger.info(request.init_time)
        # logger.info(request.user)
        return None

    def process_response(self, request, response):
        try:

            if request.user:
                userName = request.user
            else:
                userName = "null"


            #IP地址
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")

            #获取当前时间
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            #URL的消耗市场
            execute_time = round((time.time() - request.init_time),3)

            # 请求路径
            current_url = request.build_absolute_uri()

            path = request.path
            if path.endswith('jsi18n/'):
                return HttpResponse()

            # 请求方式
            method = request.method

            # 响应状态码
            status_code = response.status_code

            # 响应内容
            content = response.content
            # 记录信息
            content = str(content.decode('utf-8'))
            content = urllib.parse.unquote(content)
            # content = (json.loads(content))
            message = '%s 耗时:%s秒 用户IP:%s 用户请求URL:%s %s %s 用户名:%s' % (localtime,execute_time,ip, current_url, method, status_code,userName)
            logger.warning(message)
        except:
            logger.critical('系统错误')
        return response
