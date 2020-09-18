# -*- coding: utf-8 -*-
import json
from scrapy.spiders import Spider, Request
from pixiv_spider.settings import AUTHOR_ID
from pixiv_spider.items import ImageItem


class AuthorSpider(Spider):
    name = 'AuthorSpider'

    def start_requests(self):
        base_url = "https://www.pixiv.net/ajax/user/{user_id}/profile/all"
        url = base_url.format(user_id=AUTHOR_ID)
        yield Request(url, callback=self.parse)

    def parse(self, response):
        res_js = json.loads(response.text, encoding='utf-8')
        if res_js['error']:
            print("Response Error")
            return

        illusts = list(res_js['body']['illusts'])
        manga = list(res_js['body']['manga'])
        image = illusts + manga
        for pid in image:
            item = ImageItem()
            item['pid'] = pid
            item['author_id'] = AUTHOR_ID
            # item['author_name'] = 
            # item['title'] = 
            # print('item', item)
            yield item
