# -*- coding: UTF-8 -*-

from string import Template

reason = Template('${classname} : ${expression}')


class SpiderOneUserException(Exception):
    '''
    解析图书评分异常
    '''
    def __init__(self, expression):
        Exception.__init__(self)
        self.expression = expression

    def __str__(self):
        return reason.substitute(classname = SpiderOneUserException.__name__, expression=self.expression)


class GetBookNumberException(Exception):
    '''
    获取阅读图书数量异常
    '''
    def __init__(self, expression):
        Exception.__init__(self)
        self.expression = expression

    def __str__(self):
        return reason.substitute(classname=GetBookNumberException.__name__, expression=self.expression)

class GetBookPageException(Exception):
    '''
    抓取图书页时异常
    '''
    def __init__(self, expression):
        Exception.__init__(self)
        self.expression = expression

    def __str__(self):
        return reason.substitute(classname=GetBookPageException.__name__, expression=self.expression)


class RequestException(Exception):
    '''
    http request请求异常
    '''
    def __init__(self, expression):
        Exception.__init__(self)
        self.expression = expression

    def __str__(self):
        return reason.substitute(classname=RequestException.__name__, expression=self.expression)
