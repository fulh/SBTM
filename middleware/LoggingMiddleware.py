import time
import json
from django.utils.deprecation import MiddlewareMixin
import urllib.parse
# 获取日志logger
import logging

logger = logging.getLogger(__name__)


class LogMiddle(MiddlewareMixin):
    # 日志处理中间件
    def process_request(self, request):
        # 存放请求过来时的时间
        request.init_time = time.time()
        # logger.info(request.init_time)
        return None

    def process_response(self, request, response):
        try:

            # if request.user.is_authenticated():
            #     userName = request.user
            # else:
            #     userName = "null"


            #IP地址
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")

            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            execute_time = round((time.time() - request.init_time),3)

            # 请求路径
            path = request.path
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
            message = '%s %s秒 %s %s %s %s' % (localtime,execute_time,ip, path, method, status_code)
            logger.info(message)
        except:
            logger.critical('系统错误')
        return response
