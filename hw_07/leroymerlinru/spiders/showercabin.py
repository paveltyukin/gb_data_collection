import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from leroymerlinru.items import LeroymerlinruItem


class ShowercabinSpider(scrapy.Spider):
    name = 'showercabin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        # Получаю ссылки на все кабинки
        shower_cabin_links = response.xpath('//div[@class="ui-product-card"]/@data-product-url').extract()
        # print(1)
        for shower_cabin_link in shower_cabin_links:
            yield response.follow(shower_cabin_link, callback=self.parse_shower_cabin)

        # Ищу зеленую кнопку для перехода на следующую страницу
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()
        if next_page:
            # Перехожу на следующую страницу, если она есть
            yield response.follow(next_page, callback=self.parse)

    def parse_shower_cabin(self, response: HtmlResponse):
        # LeroymerlinruItem
        loader = ItemLoader(item=LeroymerlinruItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1[@slot="title"]/text()')
        loader.add_xpath('article', "//span[@slot='article']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('params', "//div[@class='def-list__group']/dt/text() | //div[@class='def-list__group']/dd/text()")
        loader.add_xpath('images', "//uc-pdp-media-carousel/picture[@slot='pictures']/img/@src")

        yield loader.load_item()
