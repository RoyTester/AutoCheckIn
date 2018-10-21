#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/20 23:04
# software:PyCharm
import requests
import json
from bs4 import BeautifulSoup
import re
import time
import pymysql
import threading


def run_time(f):
    def inner_f():
        start = time.time()
        f()
        end = time.time()
        m, s = divmod((end-start), 60)
        h, m = divmod(m, 60)
        print('耗时{:02d}时{:02d}分{:02d}秒'.format(int(h), int(m), int(s)))
    return inner_f


def get_soup(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/63.0.3239.132 Safari/537.36')
    }
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    else:
        time.sleep(1)
        get_soup(url)


def get_urls():
    url = 'http://www.yanwenzi.com'
    soup = get_soup(url)
    tags = soup('ul', class_='nav')[0]('li')
    urls = [url+tag.a['href'] for tag in tags]
    titles = [tag.string for tag in tags]
    return urls, titles


def get_ywz(url):
    soup = get_soup(url)
    tags = soup('ul', class_='items')[0]('li')
    ywzs = [i.p.string for i in tags]
    ywz_texts = [i.div.string for i in tags]
    if soup('div', class_='page'):
        page_tags = soup('div', class_='page')[0]
        all_page = max([int(i.string) for i in page_tags('a')])
        now_page = int(page_tags.span.string)
    else:
        return ywzs, ywz_texts, 0
    return ywzs, ywz_texts, now_page < all_page


def next_page(url):
    if not re.search('htm', url):
        url = url+'2.htm'
    else:
        # lambda 函数返回值必须为字符串
        url = re.sub('(?P<value>\d)', lambda x: str(int(x.group('value'))+1), url)
    return url


def get_ywz_dict(url, a=[], b=[]):
    ywzs, ywz_texts, bool_page = get_ywz(url)
    a.extend(ywzs)
    b.extend(ywz_texts)
    if bool_page:
        url = next_page(url)
        get_ywz_dict(url, a, b)
    return a, b


@run_time
def json_dump():
    class_dict = {}
    class_count, count = 1, 1
    urls, titles = get_urls()
    for url, title in zip(urls, titles):
        ywz_dict = {}
        print('爬取颜文字第{}类：{}'.format(class_count, title))
        class_count += 1
        a, b = get_ywz_dict(url)
        for ywz, ywz_text in zip(a, b):
            print('爬取颜文字总数{}'.format(count))
            count += 1
            ywz_dict[ywz_text] = ywz
        class_dict[title] = ywz_dict
    with open('ywz.json', 'w', encoding='utf-8') as f:
        json.dump(class_dict, f, ensure_ascii=False)


@run_time
def sql_dump():
    connect = pymysql.connect('192.168.123.1', 'root', 'admin', 'test')
    cursor = connect.cursor()
    class_count, count = 1, 1
    urls, titles = get_urls()
    for url, title in zip(urls, titles):
        print('爬取颜文字第{}类：{}'.format(class_count, title))
        class_count += 1
        try:
            cursor.execute(
                'INSERT INTO titles(title, url) values (%s, %s)', (title, url)
            )
            connect.commit()
        except:
            connect.rollback()
        cursor.execute(
            'SELECT id FROM titles WHERE title = %s', (title,)
        )
        result = cursor.fetchone()[0]
        ywzs, ywz_texts = get_ywz_dict(url)
        for ywz, ywz_text in zip(ywzs, ywz_texts):
            print('爬取颜文字总数{}'.format(count))
            count += 1
            try:
                cursor.execute(
                    'INSERT INTO ywzs(title_id, title, ywz_text, ywz) values (%s, %s, %s, %s)',
                    (result, title, ywz_text, ywz)
                )
                connect.commit()
            except:
                connect.rollback()
    connect.close()


if __name__ == '__main__':
    # json_dump()
    sql_dump()