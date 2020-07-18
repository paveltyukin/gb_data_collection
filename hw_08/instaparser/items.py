# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItemFollowers(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    follower_id = scrapy.Field()
    follower_full_name = scrapy.Field()
    follower_photo = scrapy.Field()
    type_follow = scrapy.Field()


class InstaparserItemFollowings(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    following_id = scrapy.Field()
    following_full_name = scrapy.Field()
    following_photo = scrapy.Field()
    type_follow = scrapy.Field()
