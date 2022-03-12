# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from twisted.internet import defer
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.http import HtmlResponse
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=9, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class FigshareDownloaderMiddleware:
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, IOError, TunnelError)

    def process_response(self, request, response, spider):
        """
        捕获响应不为200的请求，表示代理IP失效，则在redis数据库中删掉该代理
        """
        if response.status != 200:
            print(dir(request))
            print('url = ', request.url)
            r.rpush('figshare_plos:url', request.url)
            print('ERROR Response = ', request.meta)
        return response

    def process_exception(self, request, exception, spider):
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            print(dir(request))
            print('url = ', request.url)
            r.rpush('figshare_plos:url', request.url)
            response = HtmlResponse(url='exception')
            return response
