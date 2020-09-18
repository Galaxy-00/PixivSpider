# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    '''
    图片item
    '''
    table = collection = 'image_info'
    store_table = 'image_store'

    image_url = []
    pid = scrapy.Field()
    title = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
