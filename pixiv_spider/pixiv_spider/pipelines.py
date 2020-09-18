# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
import requests
from scrapy.exceptions import DropItem
from scrapy.http.request import Request
from pixiv_spider.settings import IMAGE_ORIGINAL, HEADERS
from scrapy.pipelines.images import ImagesPipeline
import pymysql
import pymongo


class PixivImagePipeline(ImagesPipeline):
    '''
    图片下载Pipeline
    '''
    def get_media_requests(self, item, info):
        img_url = "https://www.pixiv.net/ajax/illust/{pid}/pages".format(
            pid=item['pid'])
        res = requests.get(img_url, headers=HEADERS).text
        body = json.loads(res)['body']

        for single in body:
            if IMAGE_ORIGINAL:
                image_url = single['urls']['original']
            else:
                image_url = single['urls']['regular']

            item.image_url.append(image_url)
            yield Request(image_url)

    # def item_completed(self, results, item, info):
    #     # if not results:
    #     #     raise DropItem('下载失败')
    #     return item

    def file_path(self, request, response=None, info=None):
        url = request.url
        reg = re.match('^(.*_.*)_.*(\..*)$', url.split('/')[-1])
        file_name = reg.group(1) + reg.group(2)
        return file_name


class MysqlPipeline(object):
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.user = user
        self.port = port
        self.passwd = passwd
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
                   port=crawler.settings.get('MYSQL_PORT'),
                   user=crawler.settings.get('MYSQL_USER'),
                   passwd=crawler.settings.get('MYSQL_PASSWORD'),
                   database=crawler.settings.get('MYSQL_DATABASE'))

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host,
                                  self.user,
                                  self.passwd,
                                  self.database,
                                  charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        try:
            # 构造image_info sql
            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert into {table} ({keys}) values ({values}) on duplicate key update'.format(
                table=item.table, keys=keys, values=values)
            update = ','.join([' {key} = %s'.format(key=key) for key in data])
            sql += update
            self.cursor.execute(sql, tuple(data.values()) * 2)

            #　构造image_store sql
            image_url = item.image_url
            keys = ', '.join(['pid', 'image_url'])
            values = ', '.join(['%s'] * 2)
            store_sql = 'insert ignore into {table} ({keys}) values ({values})'.format(
                table=item.store_table, keys=keys, values=values)
            for url in image_url:
                self.cursor.execute(store_sql, tuple([item['pid'], url]))

            self.db.commit()
        except:
            self.db.rollback()

        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.collection
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()