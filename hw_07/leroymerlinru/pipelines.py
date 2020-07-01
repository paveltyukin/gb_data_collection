# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy

from scrapy.pipelines.images import ImagesPipeline
from leroymerlinru import settings
from leroymerlinru.items import LeroymerlinruItem
from pymongo import MongoClient
from os import path
from urllib.parse import urlparse


class MongoDBPipeline:

    def __init__(self):
        self.mongodb_client = MongoClient('localhost', 27017)
        self.mongodb_collection = self.mongodb_client['scrapy_parsing']['lmshowercabine']
        self.mongodb_collection.delete_many({})

    def __del__(self):
        self.mongodb_client.close()

    def process_item(self, item: LeroymerlinruItem, spider):
        self.mongodb_collection.insert_one(item)
        return item


class ShowerCabinImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return f'{request.meta["title"]}-{request.meta["article"]}/' + path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [itm[1] for itm in results if itm[0]]

        return item
