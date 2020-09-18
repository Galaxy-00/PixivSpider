import json
from scrapy.spiders import Spider, Request
from pixiv_spider.settings import USER_ID
from pixiv_spider.items import ImageItem


class BookmarkSpider(Spider):
    name = 'BookmarkSpider'

    def start_requests(self):
        limit = 48
        base_url = "https://www.pixiv.net/ajax/user/{user_id}/illusts/bookmarks?tag=&offset={offset}&limit=48&rest=show"

        for page in range(0, self.settings.get('MAX_PAGES')):
            offset = page * limit
            url = base_url.format(user_id=USER_ID, offset=offset)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        res_js = json.loads(response.text, encoding='utf-8')
        if res_js['error']:
            print("Response Error")
            return

        works = res_js['body']['works']
        for work in works:
            item = ImageItem()
            item['pid'] = work['illustId']
            item['title'] = work['illustTitle']
            item['author_id'] = work['userId']
            item['author_name'] = work['userName']
            # print('item', item)
            yield item
