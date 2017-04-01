# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
from StringIO import StringIO
from PIL import Image
import os

account_file_name = 'douban_account.log'
image_file_name = 'image.jpg'

def getSession():
    '''
    获取登录之后的session
    :return: 返回requests.Session()对象
    '''
    login_data = {'form_email': '',
                  'form_password': ''}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'https://www.douban.com/'}

    # 登陆页面
    login_url = 'https://accounts.douban.com/login'

    # 获取账号和密码
    package_dir = os.path.dirname(os.path.abspath(__file__))
    account_file = os.path.join(package_dir, account_file_name)
    with open(account_file) as f:
        login_data['form_email'] = f.readline().strip().split('|')[1]
        login_data['form_password'] = f.readline().strip().split('|')[1]

    session = requests.Session()

    # 先获取登陆页面，分析是否包含验证码
    r = session.get(login_url)
    print 'login 获取登录页面: ',r.status_code
    login_soup = BeautifulSoup(r.text, 'lxml')
    captcha_tag = login_soup.find('img', id='captcha_image')

    # 如果登陆页面有验证码识别
    if captcha_tag is not None:
        # 获取验证码图片的url
        image_url = captcha_tag['src']
        print '验证码图片地址: ',image_url

        # 保存验证码图片
        r = requests.get(image_url, stream=True)
        i = Image.open(StringIO(r.content))
        image_file = os.path.join(package_dir, image_file_name)
        i.save(image_file)

        # 获取验证码id
        captcha_input = login_soup.find(attrs={'name': 'captcha-id'})
        captcha_value = captcha_input['value']
        #print captcha_input, captcha_input['value']

        # 人工读取验证码
        captcha_key = raw_input('输入验证码: ')
        print captcha_key

        # post信息当中填充验证码
        login_data['captcha-solution'] = captcha_key
        login_data['captcha-id'] = captcha_value

    # login
    r = session.post(login_url, login_data, headers=headers)
    print 'login 登陆：',r.status_code

    return session
