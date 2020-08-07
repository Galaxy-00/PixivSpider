# -*- coding: utf-8 -*-

from scrapy.http.headers import Headers
from pixiv_spider.settings import HEADERS, COOKIE
from pixiv_spider.utils.parse_cookie import parse_cookie

class RequestMiddleware(object):
    '''
    request 中间件, 设置请求headers, cookie
    '''
    def process_request(self, request, spider):
        request.headers = Headers(HEADERS)
        request.cookies = parse_cookie(COOKIE)

