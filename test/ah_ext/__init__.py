import logging
from pyops.decorator import (make_flow, make_setup_class, make_teardown_class,
                                 make_setup, make_teardown, make_data, make_flow, alias)

logger = logging.getLogger()


def sub(x, y):
    print('....sub....')
    logger.debug("-" * 100)
    return x - y


def add(x, y):
    print('add')
    return x + y


@make_flow
def call_add(data):
    data['actual'] = add(data['x'], data['y'])


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
    req = data['req']
    print(f'test config print in call_sub {req.config.get_class_config(req, "ah_name")}')


@make_setup
def sub_setup(data):
    print(f'test_data print in setup {data}')


@make_teardown
def sub_teardown(data):
    print(f'test_data print in teardown {data}')


@make_setup_class
def sub_setup_class(req):
    print(f'....print in class_setup....')
    req.config.set_class_config(req, 'ah_name', 'atmp')


@make_teardown_class
def sub_teardown_class(req):
    print(f'....print in class_teardown....')
    ah_name = req.config.get_class_config(req, 'ah_name')
    print(f'....ah_name is {ah_name}')
