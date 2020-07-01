# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Identity, Compose, MapCompose, TakeFirst


def input_article(article):
    article_number = article.split()[-1]
    if article_number.isdigit():
        article_number = int(article_number)
    return article_number


def input_price(price):
    price_number = price.replace(' ', '')
    if price_number.isdigit():
        price_number = int(price_number)
    return price_number


def input_params(params):
    return params.strip()


def output_params(params):
    return dict(zip(params[::2], params[1::2]))


class LeroymerlinruItem(scrapy.Item):

    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(input_processor=MapCompose(input_article), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(input_price), output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(input_params), output_processor=Compose(output_params))
    images = scrapy.Field()
