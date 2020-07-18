# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from instaparser.items import InstaparserItemFollowers, InstaparserItemFollowings


class MongoDBPipeline:

    def __init__(self):
        self.mongodb_client = MongoClient('localhost', 27017)
        self.mongodb_collection = self.mongodb_client['scrapy_parsing']['instaparser']
        self.mongodb_collection.delete_many({})

    def __del__(self):
        self.mongodb_client.close()

    def process_item(self, item, spider):
        print(item)
        self.mongodb_collection.insert_one(item)
        return item
