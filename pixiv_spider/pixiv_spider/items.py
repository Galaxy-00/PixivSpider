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
    connections = 'images'
    
    pid = scrapy.Field()
    title = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
