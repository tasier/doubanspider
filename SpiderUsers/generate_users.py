# -*- coding: UTF-8 -*-

import login
from string import Template
from bs4 import BeautifulSoup
import random
from time import sleep

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'https://www.douban.com/'}

# 关注人url
douban_contacts_url = Template('https://www.douban.com/people/${userid}/contacts')
# 被关注人url
douban_rev_contacts_url = Template('https://www.douban.com/people/${userid}/contacts')


class SessionManager(object):
    session = None

    @classmethod
    def getSession(cls):
        session = SessionManager.session
        if session is None:
            SessionManager.session = login.getSession()
            print '获取session成功'
        return SessionManager.session


def getContactsUrlOfUserid(userid):
    '''
    获取用户userid的contacts_url
    :param userid: 用户id
    :return: url
    '''
    return douban_contacts_url.substitute(userid=userid)


def getRevcontactsUrlOfUserid(userid):
    '''
    获取用户userid的rev_contacts_url
    :param userid: 用户id
    :return: url
    '''
    return douban_rev_contacts_url.substitute(userid=userid)


def parseOneUserContacts(userid):
    '''
    解析一个用户的关注人页面
    :param userid:用户id
    :return:用户userid关注的所有人，返回set类型对象
    '''
    url = getContactsUrlOfUserid(userid)
    s = SessionManager.getSession()
    r = s.get(url, headers=headers)
    print 'parseOneUserContacts 爬取关注页面 ',url,r.status_code

    soup = BeautifulSoup(r.text, 'lxml')

    contacts_user = set()
    # 获取所有关注的人
    for tag in soup.find_all('dl', class_='obu'):
        # 提取用户主页
        tmp_url = tag.a['href']
        userid = tmp_url.split('/')[4]
        print '关注用户: ', userid
        contacts_user.add(userid)

    return contacts_user


def parseAllUsersContacts(userids):
    '''
    解析所有用户的关注人页面
    :param userid: set对象，所有需要解析的用户id
    :return:用户userids关注的所有人，返回set类型对象
    '''
    print 'parseAllUsersContacts 调用开始'

    result_contacts = set()
    for userid in userids:
        tmp_contacts = parseOneUserContacts(userid)
        result_contacts = result_contacts.union(tmp_contacts)
        # 随机等待1-2秒
        random_time = random.random()
        sleep(random_time + 2.0)

    print 'parseAllUsersContacts 调用结束'
    return result_contacts


def parseOneUserRevcontacts(userid):
    '''
    解析一个用户的被关注人页面
    :param userid:用户id
    :return:用户userid被关注的所有人，返回set类型对象
    '''
    url = douban_rev_contacts_url.substitute(userid=userid)
    s = SessionManager.getSession()
    r = s.get(url, headers=headers)
    print 'parseOneUserRevcontacts 爬取被关注页面 ',url,r.status_code

    soup = BeautifulSoup(r.text, 'lxml')

    rev_contacts_users = set()
    for tag in soup.find_all('dl', class_='obu'):
        # 提取用户主页
        tmp_url = tag.a['href']
        userid = tmp_url.split('/')[4]
        print '被关注用户: ',userid
        rev_contacts_users.add(userid)

    return rev_contacts_users


def parseAllUsersRevcontacts(userids):
    '''
    解析所有用户的被关注人页面
    :param userid: set对象，所有需要解析的用户id
    :return:用户userids关注的所有人，返回set类型对象
    '''
    print 'parseAllUsersRevcontacts 调用开始'

    result_contacts = set()
    for userid in userids:
        tmp_contacts = parseOneUserRevcontacts(userid)
        result_contacts = result_contacts.union(tmp_contacts)
        # 随机等待1-2秒
        random_time = random.random()
        sleep(random_time + 2.0)

    print 'parseAllUsersRevcontacts 调用结束'

    return result_contacts

def getInitUserids():
    '''
    获取初始的用户id集合
    :return: 返回id集合
    '''
    userids = set()
    # 小说
    userids.add('er-mao')
    # 绘本
    userids.add('moshou')
    # 哲学
    userids.add('a9652264')
    # 历史
    userids.add('nnnooo')
    # 编程
    userids.add('figure9')
    # 算法
    userids.add('lorryboy')

    return userids

def getlimitedUsers(num):
    '''
    爬出num个用户
    :param num: 需要爬取的用户个数
    :return: 返回爬取的用户集合
    '''
    print 'getlimitedUsers 调用开始'

    #将要被处理的
    spidering = getInitUserids()

    #结果集
    result_userids = set()

    #已经被处理的
    spidered = set()

    while len(result_userids) < num:
        print '将要处理用户数: ', len(spidering)

        contacts_users = parseAllUsersContacts(spidering)
        print '处理关注用户的数量: ', len(contacts_users)

        rev_contacts_users = parseAllUsersRevcontacts(spidering)
        print '处理被关注用户的数量: ', len(rev_contacts_users)

        #添加已经处理的userid
        spidered = spidered.union(spidering)
        print '已经处理用户数: ',len(spidered)

        #添加将要被处理的数据
        spidering.clear()
        spidering = spidering.union(contacts_users)
        spidering = spidering.union(rev_contacts_users)
        spidering = spidering.difference(spidered) #已经处理的不再去爬取

        result_userids = result_userids.union(spidered)
        result_userids = result_userids.union(spidering)

        print '当前结果集中的个数: ',len(result_userids)

    print 'getlimitedUsers 调用结束'
    return result_userids

def saveSpideredUsers(num):
    '''
    保存爬取的用户
    :param num: 至少有多少用户需要被保存
    '''

    userids = getlimitedUsers(num)

    with open('users.dat', 'a') as f:
        for userid in userids:
            f.write(userid+'\n')
            print 'sava ', userid


if __name__ == '__main__':
    saveSpideredUsers(2)