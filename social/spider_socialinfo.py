# -*- coding: UTF-8 -*-

import os
import random
from string import Template
from time import sleep

from .. import mylog
from bs4 import BeautifulSoup

from ..login import login_session

log = mylog.get_normal_logger('spider_socialinfo')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'https://www.douban.com/'}

# 关注人url
douban_contacts_url = Template('https://www.douban.com/people/${userid}/contacts')
# 被关注人url
douban_rev_contacts_url = Template('https://www.douban.com/people/${userid}/contacts')


def logOneUesrContacts(userid, contact_log=mylog.get_contact_logger()):
    '''
        解析一个用户的关注人页面，并打印日志
        :param userid:用户id
        :param contact_log: 打印关注好友日志的logger
        '''
    url = douban_contacts_url.substitute(userid=userid)
    try:
        s = login_session.SessionManager.getSession()
    except Exception, e:
        log.error('获取session异常 %s', str(e))
        raise Exception(e)

    try:
        r = s.get(url, headers=headers)
        log.info('爬取关注人页面: %s %s', url, r.status_code)
    except Exception, e:
        log.error('get %s 关注页面异常: %s', url, str(e))
        raise Exception(e)

    soup = BeautifulSoup(r.text, 'lxml')

    # 获取所有关注的人
    try:
        for tag in soup.find_all('dl', class_='obu'):
            # 提取用户主页
            tmp_url = tag.a['href']
            contact_userid = tmp_url.split('/')[4]
            log.info(userid + ' 关注 ' + contact_userid)
            contact_log.info(userid + ',' + contact_userid)
    except Exception, e:
        log.error('解析关注人页面 %s 异常: %s', url, e)
        raise Exception(e)

    log.info('解析 %s 关注人页面成功',userid)

def logOneUesrRevontacts(userid, rev_contact_log=mylog.get_revcontact_logger()):
    '''
        解析一个用户的被关注人页面，并打印日志
        :param userid:用户id
        :param rev_contact_log: 打印关注好友日志的logger
        '''
    url = douban_rev_contacts_url.substitute(userid=userid)
    try:
        s = login_session.SessionManager.getSession()
    except Exception, e:
        log.error('获取session异常 %s', str(e))
        raise Exception(e)

    try:
        r = s.get(url, headers=headers)
        log.info('爬取被关注人页面: %s %s', url, r.status_code)
    except Exception, e:
        log.error('get %s 被关注页面异常: %s', url, str(e))
        raise Exception(e)

    soup = BeautifulSoup(r.text, 'lxml')

    # 获取所有关注的人
    try:
        for tag in soup.find_all('dl', class_='obu'):
            # 提取用户主页
            tmp_url = tag.a['href']
            rev_contact_userid = tmp_url.split('/')[4]
            log.info(userid+' 被 '+rev_contact_userid+' 关注')
            rev_contact_log.info(rev_contact_userid+ ',' + userid )
    except Exception, e:
        log.error('解析关注人页面 %s 异常: %s', url, e)
        raise Exception(e)

    log.info('解析 %s 被关注人页面成功', userid)

def spider_social_info(filename):
    with open(filename) as f:
        for userid in f:
            try:
                logOneUesrContacts(userid.strip())
            except Exception, e:
                log.error('logOneUserContacts failed %s', userid.strip())
                pass
            random_sleep()
            try:
                logOneUesrRevontacts(userid.strip())
            except Exception, e:
                log.error('logOneUserRevcontacts failed %s', userid.strip())
                pass
            random_sleep()

def random_sleep():
    span = random.randint(3, 5)
    sleep_time = span + random.random()

    sleep(sleep_time)

if __name__ == '__main__':
    data_file_name = 'users.dat'
    package_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(package_dir, data_file_name)
    spider_social_info(data_file)
