# -*- coding: utf-8 -*-
import scrapy
# Для подсказок объекта response
from scrapy.http import HtmlResponse
# Подключаем класс из items
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'  # Имя паука
    allowed_domains = ['hh.ru']  # Домен в рамках которого работаем

    # Стартовая ссылка (точка входа)
    start_urls = [
        'https://krasnodar.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&L_save_area=true&area=113&from=cluster_area&showClusters=true']

    def parse(self, response: HtmlResponse):  # С этого метода все и начинается (в response - первый ответ)
        # Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()

        # Ищем на полученной странице ссылки на вакансии
        vacansy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        # Перебираем ссылки
        for link in vacansy_links:
            # Переходим по каждой ссылке и обрабатываем ответ методом vacansy_parse
            yield response.follow(link, callback=self.vacansy_parse)

        # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse
        yield response.follow(next_page, callback=self.parse)

    # Здесь обрабатываем информацию по вакансии
    def vacansy_parse(self, response: HtmlResponse):
        # Получаем наименование вакансии
        name_job = response.xpath('//h1/text()').extract_first()
        # Получаем зарплату в виде списка отдельных блоков
        salary_job = response.css('p.vacancy-salary span::text').extract()
        # Получаем ссылку на вакансию
        link_job = response.url
        # Передаем данные в item для создания структуры json
        yield JobparserItem(name=name_job, salary=salary_job, link=link_job)
