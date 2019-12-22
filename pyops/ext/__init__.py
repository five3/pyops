import time
import logging
from pyops.decorator import (make_check, make_flow, alias)

logger = logging.getLogger()


@alias('默认检查')
@make_check
def check(data):
    return data['actual'] == data['expect']


@alias('自定义检查')
@make_check
def custom_check(data):
    """

    :param data: 标准测试数据对象
        必填字段：$.custom_check，该字段为一个关键字名
    :return:
    """
    func_name = data['custom_check']
    logger.info(f'Get custom_check for {func_name}')

    func = data['req'].case_func[func_name]
    actual = data['actual']
    expect = data['expect']

    if isinstance(actual, list) and isinstance(expect, list):
        zipped = zip(actual, expect)
        return all([func(*z) for z in zipped])
    else:
        return func(actual, expect)


@alias("延时等待")
@make_flow
def time_wait(data):
    """
    等待n秒
    :param data: 测试数据对象，dict类型
        必填字段：$.data.time_wait,延时的数值，单位为秒
    :return:
    """
    n = int(data['time_wait'])
    while n > 0:
        logger.info(f'延时等待{n}秒')
        time.sleep(1)
        n -= 1
