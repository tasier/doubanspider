# -*- coding: UTF-8 -*-

import login

class SessionManager(object):
    session = None

    @classmethod
    def getSession(cls):
        session = SessionManager.session
        if session is None:
            SessionManager.session = login.getSession()
            print '获取session成功'
        return SessionManager.session