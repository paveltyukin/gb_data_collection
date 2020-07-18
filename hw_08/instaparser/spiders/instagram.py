# -*- coding: utf-8 -*-
import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse

from instaparser.items import InstaparserItemFollowers, InstaparserItemFollowings




# Получаем токен для авторизации
def fetch_csrf_token(text):
    matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
    return matched.split(':').pop().replace(r'"', '')


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'fyodr.raf34'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595086637:AQ1QAFe4EatuducUSWOKY+rl3TE9MZtPQgehrg8sLcH/tc9VaqqcD2fn2LjBFQktWAVMOHceWXavrXlIsQ9pu/hdqGoqQvJdm8YnsD2VBuTcBGEMULG8i9nzonribxCwOXUIkLyqkPH+du/SAWSOWNc='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # Пользователь, у которого собираем посты. Можно указать список
    parse_user = 'ai_machine_learning'
    parse_all_users = ['sai_chinnu_8143', 'hitzzgaja', 'the.one.dev', 'sarfaraz9845']
    # parse_all_users = ['sai_chinnu_8143']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    # hash для получения данных по постах с главной страницы
    posts_hash = 'eddbde960fed6bde675388aac39a3657'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    followings_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    # Первый запрос на стартовую страницу
    def parse(self, response: HtmlResponse):
        # csrf token забираем из html
        csrf_token = fetch_csrf_token(response.text)
        # заполняем форму для авторизации
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        # Проверяем ответ после авторизации
        if j_body['authenticated']:
            for one_user in self.parse_all_users:
                yield response.follow(
                    # Переходим на желаемую страницу пользователя.
                    f'/{one_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': one_user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        # Получаем id пользователя
        # user_id = self.fetch_user_id(response.text, username)
        matched = re.search(
            r'{\"id\":\"\d+\",\"username\":\"%s\"}' % username, response.text
        )
        user_id = json.loads(matched.group()).get('id')

        variables = {
            'id': user_id,
            'first': 12
        }
        # Формируем ссылку для получения данных
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
        url_followings = f'{self.graphql_url}query_hash={self.followings_hash}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )
        yield response.follow(
            url_followings,
            callback=self.user_followings_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

    # Принимаем ответ. Не забываем про параметры от cb_kwargs
    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        # Если есть следующая страница
        if page_info.get('has_next_page'):
            # Новый параметр для перехода на след. страницу
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )
        # Подписчики user_id
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        # Перебираем посты, собираем данные
        for follower in followers:
            item = InstaparserItemFollowers(
                user_id=user_id,
                follower_full_name=follower['node']['full_name'],
                follower_id=follower['node']['id'],
                follower_photo=follower['node']['profile_pic_url'],
                type_follow='follower'
            )
        yield item  # В пайплайн

    # Принимаем ответ. Не забываем про параметры от cb_kwargs
    def user_followings_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        # Если есть следующая страница
        if page_info.get('has_next_page'):
            # Новый параметр для перехода на след. страницу
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.followings_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followings_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )
        # Подписки user_id
        followings = j_data.get('data').get('user').get('edge_follow').get('edges')
        # Перебираем посты, собираем данные
        for follower in followings:
            item = InstaparserItemFollowings(
                user_id=user_id,
                following_id=follower['node']['id'],
                following_full_name=follower['node']['full_name'],
                following_photo=follower['node']['profile_pic_url'],
                type_follow='following'
            )
        yield item  # В пайплайн

# Получаем id желаемого пользователя
# def fetch_user_id(self, text, username):
#     matched = re.search(
#         r'{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
#     ).group()
#     return json.loads(matched).get('id')
