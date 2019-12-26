import logging
from pyops.decorator import (make_flow, make_setup_class, make_teardown_class,
                                 make_setup, make_teardown, make_data, make_flow, alias)

logger = logging.getLogger()


def sub(x, y):
    print('....sub....')
    return x - y


def add(x, y):
    print('....add....')
    return x + y


@make_flow
def call_add(data):
    data['actual'] = add(data['x'], data['y'])


@alias('sub测试数据')
@make_data
def sub_data(req):
    return {
        'x': 5,
        'y': 3,
        'expect': 2
    }


@alias('调用sub')
@make_flow
def call_sub(data):
    data['actual'] = sub(data['x'], data['y'])


@alias("用例初始化")
@make_setup
def setup(data):
    print(f'test_data print in setup {data}')


@alias("用例清理")
@make_teardown
def teardown(data):
    print(f'test_data print in teardown {data}')


@alias('套件初始化')
@make_setup_class
def sub_setup_class(req):
    print(f'....print in class_setup....')


@make_teardown_class
def sub_teardown_class(req):
    print(f'....print in class_teardown....')
