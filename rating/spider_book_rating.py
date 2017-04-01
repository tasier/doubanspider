# -*- coding: UTF-8 -*-

from .. import mylog
from ..myexception import SpiderOneUserException
from ..myexception import RequestException
from ..myexception import GetBookNumberException
from ..myexception import GetBookPageException
import requests
from string import Template
from bs4 import BeautifulSoup
from time import sleep
import random
import os

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'https://www.douban.com/'}
someone_collect_url = Template('https://book.douban.com/people/${userid}/collect')
someone_collect_page_url = Template(
        "https://book.douban.com/people/${userid}/collect?start=${num}&amp;sort=time&amp;rating=all&amp;filter=all&amp;mode=grid")

log = mylog.get_logger('spider_book_rating', logger_name='spider_book_rating')
book_rating_log = mylog.get_logger('book_rating', logger_name='book_rating', mode='a', formater='%(message)s')
user_book_number_log = mylog.get_logger('book_number', logger_name='book_number', mode='a', formater='%(message)s')


def spider_one_user_book_rating(userid):
    '''
    爬取用户userid的图书评分数据
    :param userid: 用户userid
    '''
    url = someone_collect_url.substitute(userid=userid)
    page_html = ''
    try:
        page_html = get_pagehtml(url)
    except Exception, e:
        raise Exception(e)

    book_number = 0
    try:
        book_number = get_userid_number_of_book(userid, page_html)
        log.info("%s 读过 %s 本书", userid, book_number)
        user_book_number_log.info("%s, %s", userid, book_number)
    except Exception, e:
        raise Exception(e)

    try:
        spider_one_user_read_books(userid, book_number)
    except Exception, e:
        raise Exception(e)


def get_pagehtml(url):
    '''
    获取url的html网页
    :param url: 网页url
    :return: 网页html
    '''
    try:
        r = requests.get(url, headers=headers)
        return r.text
    except Exception, e:
        reason = url+','+str(e)
        request_exception = RequestException(reason)
        log.error(request_exception)
        raise request_exception


def get_userid_number_of_book(userid, page_html):
    try:
        page_number = get_number_of_book(page_html)
        return page_number
    except Exception, e:
        reason = str(userid)+' '+str(e)
        get_book_number_exception = GetBookNumberException(reason)
        log.error(get_book_number_exception)
        raise get_book_number_exception


def get_number_of_book(page_html):
    '''
    确定
    :param page_html:
    :return:
    '''
    index_soup = BeautifulSoup(page_html, 'lxml')
    # 寻找读了多少本书的标签
    try:
        subject_num_tag = index_soup.find(
            lambda tag:
            cmp(tag.name, 'span') == 0  # span标签
            and tag.has_attr('class')  # 有class属性
            and cmp(tag['class'][0], 'subject-num') == 0)  # class属性为subject-num
    except Exception, e:
        reason = '无法解析读了多少本书 '+str(e)
        get_book_number_exception = GetBookNumberException(reason)
        raise get_book_number_exception

    if subject_num_tag is not None:
        # 1-15 / 158
        # 确定有多少本书
        num_of_books = int(subject_num_tag.string.split('/')[1].strip())
        return num_of_books
    else:
        return 0


def spider_one_user_read_books(userid, book_number):
    num_of_each_page = 15  # 每页抓取的数量
    for num in range(0, book_number, num_of_each_page):
        random_sleep()

        url = someone_collect_page_url.substitute(userid=userid, num=num)
        page_html = ''
        try:
            page_html = get_pagehtml(url)
        except Exception, e:
            reason = str(userid)+' '+url+' '+str(e)
            get_book_page_exception = GetBookPageException(reason)
            log.error(get_book_page_exception)
            continue

        log_one_page_book_rating(userid, page_html)


def log_one_page_book_rating(userid, page_html):
    # 处理抓取的每一个页面
    soup = BeautifulSoup(page_html, 'lxml')
    for item in soup.find_all('li', class_='subject-item'):
        # 获取评分标签
        book_rating_tag = item.find(
            lambda tag:
            cmp(tag.name, 'span') == 0  # span标签
            and tag.has_attr('class')  # 有class属性
            and tag['class'][0].startswith('rating'))  # class属性以rating开头

        # 判断rating是否有，对书有评价的话在操作
        # bookid,bookname,rating,bookpubinfo
        if book_rating_tag is not None:
            bookid = item.a['href'].split('/')[4]
            bookname = item.find('div', class_='info').a['title']
            rating = book_rating_tag['class'][0][6]
            bookpubinfo = item.find('div', class_='pub').string.strip()

            book_rating_log.info('%s, %s, %s, %s, %s', userid, bookid, bookname, rating, bookpubinfo)
            log.info('%s, %s, %s, %s, %s', userid, bookid, bookname, rating, bookpubinfo)


def spider_all_users(filename):
    with open(filename) as f:
        for line in f:
            try:
                spider_one_user_book_rating(line.strip())
                random_sleep()
            except Exception, e:
                reason = line.strip()+' '+str(e)
                user_failed_exception = SpiderOneUserException(reason)
                log.error(user_failed_exception)


def random_sleep():
    span = random.randint(2, 4)
    sleep_time = span + random.random()

    sleep(sleep_time)

if __name__ == '__main__':
    filename = 'users_small235.csv'
    package_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(package_dir, filename)
    spider_all_users(data_file)
