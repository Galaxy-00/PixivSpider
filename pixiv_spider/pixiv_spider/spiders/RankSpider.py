# -*- coding: utf-8 -*-
import json
from scrapy.spiders import Spider, Request
from pixiv_spider.settings import MAX_PAGES, MODE
from pixiv_spider.items import ImageItem


class RankSpider(Spider):
    name = 'RankSpider'

    def start_requests(self):
        base_url = "https://www.pixiv.net/ranking.php?mode={mode}&p={page}&format=json"
        for page in range(1, MAX_PAGES + 1):
            url = base_url.format(mode=MODE, page=page)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        res_js = json.loads(response.text, encoding='utf-8')
        if res_js == None:
            print('response is None')
            return

        contents = res_js['contents']
        for single in contents:
            item = ImageItem()
            item['pid'] = single['illust_id']
            item['title'] = single['title']
            item['author_name'] = single['user_name']
            item['author_id'] = single['user_id']
            print('item', item)
            yield item
