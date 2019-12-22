#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-25 14:51:15
# @Author  : Xiaowu Chen (chenxiaowu@autohome.com.cn)
# @Link    : https://five3.blog.csdn.net/
# @Version : $Id$
import functools


def make(key='flow'):
    def make_key(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if hasattr(wrapper, 'ah_type'):
            wrapper.ah_type.append(key)
        else:
            wrapper.ah_type = [key]
        return wrapper

    return make_key


make_setup_class = make(key='setup_class')
make_setup = make(key='setup')
make_data = make(key='data')
make_flow = make(key='flow')
make_check = make(key='check')
make_teardown = make(key='teardown')
make_teardown_class = make(key='teardown_class')


def alias(name=None):
    def make_alias(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.alias = name
        return wrapper

    return make_alias
