# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe.f-test-link-Dalshe::attr(href)').extract_first()
        vacancy_links = response.css('div._3zucV._1fMKr div._3mfro.PlM3e._2JVkc._3LJqf a.icMQ_._6AfZ9::attr(href)').extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        # Получаем наименование вакансии
        name_job = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first()
        # Получаем зарплату в виде списка отдельных блоков
        salary_job = response.css('span._1OuF_.ZON4b span._3mfro._2Wp8I.PlM3e._2JVkc::text').extract()
        # Получаем ссылку на вакансию
        link_job = response.url
        print(1)
        yield JobparserItem(name=name_job, salary=salary_job, link=link_job)
