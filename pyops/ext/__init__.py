import time
import logging
from pyops.decorator import (make_check, make_flow, alias)

logger = logging.getLogger()


@alias('默认检查')
@make_check
def check(init_data, run_data, global_data):
    return run_data['actual'] == init_data['expect']


@alias('自定义检查')
@make_check
def custom_check(int_data, run_data, global_data):
    func_name = global_data['custom_check']
    logger.info(f'Get custom_check for {func_name}')

    func = global_data['request'].case_func[func_name]
    actual = run_data['actual']
    expect = int_data['expect']

    if isinstance(actual, list) and isinstance(expect, list):
        zipped = zip(actual, expect)
        return all([func(*z) for z in zipped])
    else:
        return func(actual, expect)


@alias("延时等待")
@make_flow
def time_wait(int_data, run_data, global_data):
    """
    等待n秒
    :param data: 测试数据对象，dict类型
        必填字段：$.data.time_wait,延时的数值，单位为秒
    :return:
    """
    n = int(int_data['time_wait'])
    while n > 0:
        logger.info(f'延时等待{n}秒')
        time.sleep(1)
        n -= 1
