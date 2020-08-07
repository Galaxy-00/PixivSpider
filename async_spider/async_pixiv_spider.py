# %%
import os
import json
import time
import asyncio
import requests
from re import error
from loguru import logger
from retrying import retry
from scrapy import Selector
from datetime import datetime
from urllib.parse import urlencode
from aiohttp.client import ClientSession


class PixivSpider(object):
    '''
    Pixiv爬虫
    '''
    def __init__(self, cookie, enable_save_log=False) -> None:
        '''
        初始化爬虫
        :param cookie: 登录后的cookie
        :param enable_save_log: 是否启用日志, 启用后生成日志文件, 默认为否
        '''
        self.headers = {
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": "https://www.pixiv.net/login.php",
            "Origin": "https://accounts.pixiv.net",
            "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Cookie": cookie
        }
        self.enable_save_log = enable_save_log
        self.user_home_url = "https://www.pixiv.net/users/{user_id}"
        self.user_url = "https://www.pixiv.net/ajax/user/{user_id}/profile/all"
        self.user_bookmarks_url = "https://www.pixiv.net/ajax/user/{user_id}/illusts/bookmarks?tag=&offset={offset}&limit={limit}&rest=show"
        self.artwork_url = "https://www.pixiv.net/ajax/illust/{pid}/pages"
        self.ranking_url = "https://www.pixiv.net/ranking.php?mode={mode}&p={page}&format=json"
        self.ranking_content_url = "https://www.pixiv.net/ranking.php?mode={mode}&content={content}&p={page}&format=json"
        self.tag_url = 'https://www.pixiv.net/ajax/search/artworks/{key_word}?p={page}&{params}'

    @logger.catch
    @retry(stop_max_attempt_number=3,
           wait_random_min=600,
           wait_random_max=1500)
    async def __async_get_page(self, url, is_bytes=False):
        '''
        异步请求页面
        尝试请求3次, 每次最短等待600ms, 最长等待1.5s
        :param url: 请求页面url
        :param is_bytes: 是否返回二进制数据, 用于存储图像, 默认返回text
        '''
        try:
            async with ClientSession() as session:
                async with session.get(url, headers=self.headers) as res:
                    if is_bytes:
                        return await res.read()
                    return await res.text()
        except Exception as e:
            logger.error("!!! Crawling Url: {} Failed, Reason: {} !!!".format(
                url, e))

    @logger.catch
    @retry(stop_max_attempt_number=3,
           wait_random_min=600,
           wait_random_max=1500)
    def __get_page(self, url, is_bytes=False):
        '''
        请求页面
        尝试请求3次, 每次最短等待600ms, 最长等待1.5s
        :param url: 请求页面url
        :param is_bytes: 是否返回二进制数据, 用于存储图像, 默认返回text
        '''
        try:
            res = requests.get(url, headers=self.headers)
            if is_bytes:
                return res.content
            return res.text
        except Exception as e:
            logger.error("!!! Crawling Url: {} Failed, Reason: {} !!!".format(
                url, e))

    @logger.catch
    def __store_image(self, image_data, image_name, dir_path):
        '''
        将图像以其名字存储到对应目录中
        :param image_data: 图像二进制数据
        :param image_name: 图像存储名字
        :param dir_path: 存储路径
        '''
        try:
            # 是否存在目录, 否则创建
            if os.path.exists(dir_path):
                pass
            else:
                os.mkdir(dir_path)
            if image_data != None:
                with open(os.path.join(dir_path, image_name), 'wb') as f:
                    f.write(image_data)
            else:
                raise Exception('Image Data is None')
        except Exception as e:
            logger.error("!!!  Store Failed, Reason: {} !!!".format(e))

    @logger.catch
    async def __async_get_art_by_pid(self,
                                     pid,
                                     dir_path='image',
                                     is_original=False):
        '''
        异步爬取pid的图片
        :param pid: 图片pid
        :param dir_path: 存储路径, 默认为当前目录的image
        :param is_original: 是否存储原图, 默认存储regual
        '''
        try:
            start_time = datetime.now()
            pid = str(pid)
            logger.info('--- Crawling Image Pid: {pid} ---'.format(pid=pid))

            body = json.loads(await self.__async_get_page(
                self.artwork_url.format(pid=pid)))['body']
            image_url = ''
            for ill_num in range(0, len(body)):
                if is_original:
                    image_url = body[ill_num]["urls"]["original"]
                else:
                    image_url = body[ill_num]["urls"]["regular"]

                if len(body) != 1:
                    store_name = "{pid}_{num}{type}".format(
                        pid=pid, num=ill_num, type=image_url[-4:])
                else:
                    store_name = "{pid}{type}".format(pid=pid,
                                                      type=image_url[-4:])
                # 是否以及保存了该artwork
                if not os.path.exists(os.path.join(dir_path, store_name)):
                    image_data = await self.__async_get_page(image_url, True)
                    self.__store_image(image_data, store_name, dir_path)
                    logger.info(
                        '--- Store Image Pid: {}, Num: {}, Using Time: {}s ---'
                        .format(pid, ill_num,
                                (datetime.now() - start_time).seconds))
                else:
                    logger.info(
                        '--- Image Pid: {} , Num: {} Already Exists ---'.
                        format(pid, ill_num))

            logger.info('vvv Image Pid: {} Done vvv'.format(pid))
        except Exception as e:
            logger.error("!!! Get Image Failed, Reason: {} !!!".format(e))

    @logger.catch
    def get_art_by_pid(self, pid, dir_path='image', is_original=False):
        '''
        爬取pid的图片
        :param pid: 图片pid
        :param dir_path: 存储路径, 默认为当前目录的image
        :param is_original: 是否存储原图, 默认存储regular
        '''
        try:
            start_time = datetime.now()
            pid = str(pid)
            logger.info('--- Crawling Image Pid: {pid} ---'.format(pid=pid))
            res = self.__get_page(self.artwork_url.format(pid=pid))
            body = json.loads(res)["body"]

            image_url = ''
            for ill_num in range(0, len(body)):
                if is_original:
                    image_url = body[ill_num]["urls"]["original"]
                else:
                    image_url = body[ill_num]["urls"]["regular"]
                if len(body) != 1:
                    store_name = "{pid}_{num}{type}".format(
                        pid=pid, num=ill_num, type=image_url[-4:])
                else:
                    store_name = "{pid}{type}".format(pid=pid,
                                                      type=image_url[-4:])

                if not os.path.exists(os.path.join(dir_path, store_name)):
                    image_data = self.__get_page(image_url, True)
                    self.__store_image(image_data, store_name, dir_path)
                    logger.info(
                        '--- Store Image Pid: {}, Num: {}, Using Time: {}s ---'
                        .format(pid, ill_num,
                                (datetime.now() - start_time).seconds))
                else:
                    logger.info(
                        '--- Image Pid: {} , Num: {} Already Exists ---'.
                        format(pid, ill_num))

            logger.info('vvv Crawling Image Pid: {} Done vvv'.format(pid))
        except Exception as e:
            logger.error("!!! Get Image Failed, Reason: {} !!!".format(e))

    @logger.catch
    def get_arts_by_author_id(self, author_id, is_original=False):
        '''
        爬取id作者的作品
        :param author_id: id
        :param is_original: 是否存储原图, 默认存储regular
        '''
        try:
            logger.info(
                '::: Crawling Author Id: {} Artworks :::'.format(author_id))

            # 获取作者插画和漫画ｐｉｄ
            res = self.__get_page(self.user_url.format(user_id=author_id))
            res_js = json.loads(res)
            illusts_id = list(res_js['body']['illusts'])
            manga_id = list(res_js['body']['manga'])
            image_id = illusts_id + manga_id

            # 尝试从pickup中获取author_name
            pickup = res_js['body']['pickup']
            if len(pickup):
                author_name = pickup[0]['userName']
            else:
                # 不存在则从home page中获取author_name
                author_name = json.loads(
                    Selector(text=self.__get_page(
                        self.user_home_url.format(user_id=author_id))).css(
                            'meta[name="preload-data"]::attr(content)').
                    extract_first())['user'][str(author_id)]['name']

            store_dir = '{name}_{id}'.format(name=author_name, id=author_id)

            if self.enable_save_log:
                # 日志存储
                logger.add(
                    os.path.join(
                        store_dir, '{name}_{id}.log'.format(name=author_name,
                                                            id=author_id)))

            # 异步爬取
            loop = asyncio.get_event_loop()
            tasks = [
                loop.create_task(
                    self.__async_get_art_by_pid(image_id[i], store_dir,
                                                is_original))
                for i in range(0, len(image_id))
            ]
            loop.run_until_complete(asyncio.wait(tasks))

            logger.info('vvv Crawling Name: {}, Id: {} Done vvv'.format(
                author_name, author_id))
        except Exception as e:
            logger.error(
                "!!! Get Author Image Failed, Reason: {} !!!".format(e))

    @logger.catch
    def get_arts_by_rank(self, mode, content, crawl_page, is_original=False):
        '''
        异步爬取排行榜
        :param mode: daily weekly monthly rookie新人 original原创 male female daily_r18 weekly_r18 male_r18 female_r18
        :param content: all综合 illust插画 ugoira动图 manga漫画
        :param crawl_page: 要爬取几页
        :param is_original: 是否存储原图, 默认存储regular
        '''
        if mode not in [
                'daily', 'weekly', 'monthly', 'rookie', 'original', 'male',
                'female', 'daily_r18', 'weekly_r18', 'male_r18', 'female_r18'
        ]:
            raise error(
                "The mode must be one of ''daily', 'weekly', 'monthly', 'rookie', 'original', 'male', 'female', 'daily_r18', 'weekly_r18', 'male_r18', 'female_r18''"
            )
        if content not in ['all', 'illust', 'ugoira', 'manga']:
            raise error(
                "The content must be one of ''all', 'illust', 'ugoira', 'manga''"
            )
        try:
            crawl_date = time.strftime("%Y-%m-%d", time.localtime())
            store_dir = '{mode}_{date}'.format(mode=mode, date=crawl_date)

            if self.enable_save_log:
                logger.add(
                    os.path.join(
                        store_dir,
                        '{mode}_{content}.log'.format(mode=mode,
                                                      content=content)))

            for i in range(1, crawl_page + 1):
                if content == 'all':
                    ranking_url = self.ranking_url.format(mode=mode, page=i)
                else:
                    ranking_url = self.ranking_content_url.format(
                        page=i, mode=mode, content=content)

                logger.info(
                    '::: Crawling Mode: {} Content: {} Ranking Page: {} :::'.
                    format(mode, content, crawl_page))
                res_js = json.loads(self.__get_page(ranking_url))

                # 异步爬取
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.create_task(
                        self.__async_get_art_by_pid(
                            res_js['contents'][j]['illust_id'], store_dir,
                            is_original))
                    for j in range(0, len(res_js['contents']))
                ]
                loop.run_until_complete(asyncio.wait(tasks))

            logger.info(
                'vvv Crawling Ranking: {mode} Done vvv'.format(mode=mode))
        except Exception as e:
            logger.error('!!! Get Ranking Failed, Reason: {} !!!'.format(e))

    @logger.catch
    def get_user_bookmarks(self, user_id, is_original=False):
        '''
        异步获取用户id的收藏
        :param user_id: 用户id
        :param is_original: 是否存储原图, 默认存储regular
        '''
        try:
            offset, limit = 0, 48
            store_dir = 'bookmarks_{}'.format(user_id)

            if self.enable_save_log:
                logger.add(
                    os.path.join(store_dir,
                                 'bookmarks_{}.log'.format(user_id)))

            total_image = json.loads(
                self.__get_page(
                    self.user_bookmarks_url.format(
                        user_id=user_id, offset=offset,
                        limit=limit)))['body']['total']
            logger.info(
                '::: Crawling User: {} Bookmarks, Total: {} :::'.format(
                    user_id, total_image))

            for offset in range(0, total_image, limit):
                logger.info(
                    '::: Crawling Bookmarks Offset: {} :::'.format(offset))
                res_js = json.loads(
                    self.__get_page(
                        self.user_bookmarks_url.format(user_id=user_id,
                                                       offset=offset,
                                                       limit=limit)))
                works = res_js['body']['works']

                # 异步爬取
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.create_task(
                        self.__async_get_art_by_pid(work['illustId'],
                                                    store_dir, is_original))
                    for work in works
                ]
                loop.run_until_complete(asyncio.wait(tasks))

            logger.info(
                'vvv Crawling User: {} Bookmarks Number: {} Done vvv'.format(
                    user_id, total_image))
        except Exception as e:
            logger.error('!!! Get User Bookmarks Error: {} !!!'.format(e))

    @logger.catch
    def get_arts_by_tag(self, tags, pages, is_original=False, **kwargs):
        '''
        根据tags来获取artworks
        :param tags: list类型, 图片的tag, 日文, 需要排除的tag前加'-'号
        :param pages: 要爬取的页数
        :param is_original: 是否存储原图, 默认存储regular
        :param **kwargs:
        :param order: date_d(默认), date
        :param mode: all(默认), safe, r18
        :param s_mode: s_tag(标签部分一致, 默认) s_tag_full(全部一致) s_tc(标题,说明文字)
        :param type: all(默认) illust_and_ugoira(illust) illust(illust) manga ugoira
        :param scd: 制定起始范围(例: 2020-7-10)
        :param ecd: 制定结束范围
        '''
        try:
            key_word = ""
            for tag in tags:
                key_word += tag + " "
            key_word = key_word[:-1]
            kwargs.update({"word": key_word})
            crawl_url = self.tag_url.format(key_word=key_word,
                                            page=1,
                                            params=urlencode(kwargs))
            logger.info('::: Crawling Tags: {}, Params: {} :::'.format(
                key_word, kwargs))

            res_js = json.loads(self.__get_page(crawl_url))
            tag_type, total = "", ""
            if "type" not in kwargs or kwargs["type"] == "all":
                total = res_js['body']['illustManga']["total"]
                tag_type = "illustManga"
            elif kwargs["type"] == "illust_and_ugoira" or kwargs[
                    "type"] == "illust":
                total = res_js['body']['illust']["total"]
                tag_type = "illust"
            elif kwargs["type"] == "manga":
                total = res_js['body']["manga"]["total"]
                tag_type = "manga"
            elif kwargs["type"] == "ugoira":
                total = res_js['body']["ugoira"]["total"]
                tag_type = "ugoira"
            logger.info('::: Tag Has Total: {} illusts :::'.format(total))

            store_dir = key_word
            if self.enable_save_log:
                # 日志存储
                logger.add(os.path.join(store_dir, '{}.log'.format(store_dir)))

            for page in range(1, pages + 1):
                logger.info(
                    '::: Crawling Page: {}, Tags: {}, Params: {} :::'.format(
                        page, key_word, kwargs))
                res = self.__get_page(
                    self.tag_url.format(key_word=key_word,
                                        page=page,
                                        params=urlencode(kwargs)))
                if res == None:
                    raise Exception("Crawling Page Return None")
                data = json.loads(res)['body'][tag_type]['data']

                loop = asyncio.get_event_loop()
                tasks = [
                    loop.create_task(
                        self.__async_get_art_by_pid(single['illustId'],
                                                    store_dir, is_original))
                    for single in data if 'illustId' in single
                ]
                loop.run_until_complete(asyncio.wait(tasks))

            logger.info(
                'vvv Crawl Tags: {}, Params: {}, Pages: {} Done vvv'.format(
                    key_word, kwargs, pages))
        except Exception as e:
            logger.error("!!! Crawl Error: {} !!!".format(e))


# %%
if __name__ == '__main__':
    pid = 81691228
    try:
        with open("cookie.txt", "r") as f:
            cookie = f.read()
        spider = PixivSpider(cookie, True)
        spider.get_art_by_pid(pid)
    except Exception as e:
        print('--- Error: {} ---'.format(e))
