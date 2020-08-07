# -*- coding: utf-8 -*-

from scrapy.http.headers import Headers
from pixiv_spider.settings import COOKIE
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from pixiv_spider.settings import HEADERS, COOKIE
from pixiv_spider.utils.parse_cookie import parse_cookie

class RequestMiddleware(object):

    def process_request(self, request, spider):
        request.headers = Headers(HEADERS)
        request.cookies = parse_cookie(COOKIE)

