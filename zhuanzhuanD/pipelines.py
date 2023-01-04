# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import time

from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient

from zhuanzhuanD.settings import MONGODB_URL, BOT_NAME
from zhuanzhuanD.spiders.zhuanzhuan import ZhuanzhuanSpider

class ZhuanzhuandPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(f"https:{item['mainImg']}")

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        adapter = ItemAdapter(item)
        adapter['file_paths'] = file_paths[0]
        return item
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     print('**********products/' + time.time() + ".jpg")
    #     image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
    #     image_perspective = request.url.split('/')[-2]
    #     image_filename = f'{image_url_hash}_{image_perspective}.jpg'
    #
    #     return image_filename
    #     # print('**********products/' + time.time() + ".jpg")
    #     # return f"products/{str(time.time())}.jpg"
    # def process_item(self, item, spider):
    #     return item
class MongoPipeline:
    def open_spider(self, spider):
        if isinstance(spider, ZhuanzhuanSpider):
            self.client = MongoClient(MONGODB_URL)
            self.collection = self.client[BOT_NAME]["iphone"]

    def process_item(self, item, spider):
        if isinstance(spider, ZhuanzhuanSpider):
            self.collection.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        if isinstance(spider, ZhuanzhuanSpider):
            self.client.close()