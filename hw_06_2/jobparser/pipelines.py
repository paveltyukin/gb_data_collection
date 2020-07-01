# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


def get_full_salary_sj(salary):
    full_salary = {
        'min': 0,
        'max': 0
    }

    if len(salary) == 4:
        full_salary['min'] = salary[0].replace('\xa0', '')
        full_salary['max'] = salary[1].replace('\xa0', '')
        return full_salary

    if salary[0].find('договорённости') != -1 and len(salary) == 1:
        full_salary['min'] = None
        full_salary['max'] = None
        return full_salary

    if salary[0].find('от') != -1:
        full_salary['min'] = ''.join(salary[2].replace('\xa0', ' ').split()[:-1])
        full_salary['max'] = None
        return full_salary

    if salary[0].find('до') != -1:
        full_salary['min'] = ''.join(salary[2].replace('\xa0', ' ').split()[:-1])
        full_salary['max'] = None
        return full_salary


def get_full_salary_hh(salary):
    salary = " ".join(salary)
    salary = salary.replace('\xa0', '')
    salary = salary.replace('  ', ' ')

    full_salary = {
        'min': 0,
        'max': 0
    }

    if (salary.find('до') == -1) and (salary.find('от') == -1):
        full_salary['min'] = None
        full_salary['max'] = None
        return full_salary

    if salary.find('до') == 0:
        full_salary['min'] = None
        full_salary['max'] = salary.split()[1]
        return full_salary

    if salary.find('от') == 0:
        if salary.find('до') == -1:
            full_salary['min'] = salary.split()[1]
            full_salary['max'] = None
            return full_salary
        else:
            full_salary['min'] = salary.split()[1]
            temp_salary = salary[salary.find('до') + 3:].split()[0]
            if temp_salary.isdigit():
                full_salary['max'] = temp_salary
            else:
                full_salary['max'] = None
            return full_salary


class JobparserPipeline:
    # Конструктор, где инициализируем подключение к СУБД
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_parsing

    # Метод, куда прилетает сформированный item
    def process_item(self, item, spider):
        dict_vacancy = {}
        if spider.name == 'hhru':
            full_salary = get_full_salary_hh(item['salary'])
            dict_vacancy['name'] = item['name']
            dict_vacancy['link'] = item['link']
            dict_vacancy['salary'] = {
                'min': full_salary['min'],
                'max': full_salary['max']
            }
        else:
            full_salary = get_full_salary_sj(item['salary'])
            dict_vacancy['name'] = item['name']
            dict_vacancy['link'] = item['link']
            dict_vacancy['salary'] = {
                'min': full_salary['min'],
                'max': full_salary['max']
            }

        collection = self.mongo_base[spider.name]
        collection.insert_one(dict_vacancy)
        print(dict_vacancy)
        return item
