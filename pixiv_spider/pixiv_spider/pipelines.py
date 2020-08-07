# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests
from scrapy.exceptions import DropItem
from scrapy.http.request import Request
from pixiv_spider.settings import IMAGE_ORIGINAL, HEADERS
from scrapy.pipelines.images import ImagesPipeline


class ImagePipeline(ImagesPipeline):
    '''
    图片下载Pipeline
    '''
    def get_media_requests(self, item, info):
        img_url = "https://www.pixiv.net/ajax/illust/{pid}/pages".format(pid=item['pid'])
        res = requests.get(img_url, headers=HEADERS).text
        body = json.loads(res)['body']

        for ill_num in range(0, len(body)):
            if IMAGE_ORIGINAL:
                image_url = body[ill_num]['urls']['original']
            else:
                image_url = body[ill_num]['urls']['regular']
            yield Request(image_url)

    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        # if not results:
        #     raise DropItem('下载失败')
        return item

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
