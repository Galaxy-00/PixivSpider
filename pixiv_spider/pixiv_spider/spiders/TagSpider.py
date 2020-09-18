# -*- coding: utf-8 -*-
import json
from scrapy.spiders import Spider, Request
from pixiv_spider.settings import MAX_PAGES, TAG_MODE, KEY_WORD
from pixiv_spider.items import ImageItem
from urllib.parse import urlencode


class TagSpider(Spider):
    name = 'TagSpider'

    def start_requests(self):
        base_url = 'https://www.pixiv.net/ajax/search/artworks/{key_word}?p={page}&{params}'
        key_word, mode = KEY_WORD, TAG_MODE
        params = {'mode': mode, 'word': key_word}
        for page in range(1, MAX_PAGES + 1):
            url = base_url.format(key_word=key_word,
                                  page=page,
                                  params=urlencode(params))
            yield Request(url, callback=self.parse)

    def parse(self, response):
        res_js = json.loads(response.text, encoding='utf-8')
        if res_js['error']:
            print(res_js['message'])
            return

        data = res_js['body']['illustManga']["data"]
        for single in data:
            if 'illustId' in single:
                item = ImageItem()
                item['pid'] = single['illustId']
                item['title'] = single['illustTitle']
                item['author_name'] = single['userName']
                item['author_id'] = single['userId']
                # print('item', item)
                yield item
