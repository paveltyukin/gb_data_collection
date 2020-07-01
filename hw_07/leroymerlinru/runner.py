# Импортируем класс для создания процесса
from scrapy.crawler import CrawlerProcess
# Импортируем класс для настроек
from scrapy.settings import Settings
# Наши настройки
from leroymerlinru import settings
# Класс паука
from leroymerlinru.spiders.showercabin import ShowercabinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ShowercabinSpider, search='душевая кабина')
    process.start()
