# -*- coding: UTF-8 -*-

import logging
import os
from string import Template

#创建日志目录
log_dir = 'log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def get_logger(log_filename, logger_name='normal_logger', mode='w', formater='%(asctime)s -%(name)s  %(levelname)s:%(message)s'):
    if not isinstance(log_filename, str):
        print 'not a valid log_filename'
        raise Exception('not a valid log_filename')

    log_file = Template('log/${log_filename}.log')

    # 普通log
    formatter = logging.Formatter(formater)
    normal_logger = logging.getLogger(logger_name)
    normal_file_handler = logging.FileHandler(log_file.substitute(log_filename=log_filename), mode=mode)
    normal_file_handler.setFormatter(formatter)
    normal_logger.addHandler(normal_file_handler)

    normal_logger.setLevel(logging.DEBUG)

    return normal_logger


def get_contact_logger():
    formatter = logging.Formatter('%(message)s')
    # 关注用户logger
    contact_logger = logging.getLogger('contact_logger')
    contact_file_handler = logging.FileHandler('log/contact.log')
    contact_file_handler.setFormatter(formatter)
    contact_logger.addHandler(contact_file_handler)

    contact_logger.setLevel(logging.DEBUG)

    return contact_logger


def get_revcontact_logger():
    formatter = logging.Formatter('%(message)s')
    # 关注用户logger
    revcontact_logger = logging.getLogger('rev_contact_logger')
    revcontact_file_handler = logging.FileHandler('log/revcontact.log')
    revcontact_file_handler.setFormatter(formatter)
    revcontact_logger.addHandler(revcontact_file_handler)

    revcontact_logger.setLevel(logging.DEBUG)

    return revcontact_logger