import pytest
import logging
from .base import *

logger = logging.getLogger()


@pytest.fixture
def test_data(request):
    print("=" * 30)

    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run test_data => [{module}.{cls}.{func}]')
    data = get_data_by_func_name(func, cls, module, request)
    data['req'] = request
    logger.info(f'end test_data => [{module}.{cls}.{func}]')

    data['test_data'] = True
    yield data


@pytest.fixture
def test_flow(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run test_flow => [{module}.{cls}.{func}]')
    flow = get_flow_by_func_name(func, cls, module, request)
    for f in flow:
        if f.__code__.co_argcount == 2:
            status = f(test_data, request)
        else:
            status = f(test_data)

        if status is False:
            test_data['result'] = False
            test_data['msg'] = f"execute flow {f.__name__} Failed."
            break
    logger.info(f'end test_flow => [{module}.{cls}.{func}]')

    test_data['test_flow'] = True
    yield flow


@pytest.fixture
def test_check(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run test_check => [{module}.{cls}.{func}]')
    if 'result' in test_data:
        logger.info(f'test_check msg => [{test_data["msg"]}]')
        assert test_data['result']
        check = None
    else:
        check = get_check_by_func_name(func, cls, module, request)
        for f in check:
            if f.__code__.co_argcount == 2:
                assert f(test_data, request)
            else:
                assert f(test_data)
    logger.info(f'end test_check => [{module}.{cls}.{func}]')

    test_data['test_check'] = True
    yield check


@pytest.fixture
def init(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run setup => [{module}.{cls}.{func}]')
    init = get_init_by_name(cls, module, request)
    for f in init:
        if f.__code__.co_argcount == 2:
            status = f(test_data, request)
        else:
            status = f(test_data)

        if status is False:
            raise ValueError(f"setup failed for [{module}.{cls}.{func}]")
    logger.info(f'end setup => [{module}.{cls}.{func}]')

    test_data['init'] = True
    yield None


@pytest.fixture
def dest(request, test_data):
    yield None
    test_data['dest'] = True

    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run teardown => [{module}.{cls}.{func}]')
    dest = get_dest_by_name(cls, module, request)
    for f in dest:
        if f.__code__.co_argcount == 2:
            status = f(test_data, request)
        else:
            status = f(test_data)

        if status is False:
            raise ValueError(f"teardown failed for [{module}.{cls}.{func}]")

    logger.info(f'end teardown => [{module}.{cls}.{func}]')


@pytest.fixture(scope="class")
def class_init(request):
    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run setup_class => [{module}.{cls}]')
    dest = get_class_init_by_name(cls, module, request)
    # 初始化全局设置
    request.config.ah_class_config = get_global_config(cls, module, request)
    # 绑定全局设置方法
    request.get_global = get_class_config
    request.set_global = set_class_config
    request.del_global = del_class_config
    request.clear_global = clear_class_config

    for f in dest:
        status = f(request)
        if status is False:
            raise ValueError(f"setup failed for [{module}.{cls}]")

    logger.info(f'end setup_class => [{module}.{cls}]')

    yield None


@pytest.fixture(scope="class")
def class_dest(request):
    yield None

    cls = request.cls.__name__
    module = request.module.__name__

    logger.info(f'run teardown_class => [{module}.{cls}]')
    dest = get_class_dest_by_name(cls, module, request)
    for f in dest:
        status = f(request)
        if status is False:
            raise ValueError(f"teardown failed for [{module}.{cls}]")

    logger.info(f'end teardown_class => [{module}.{cls}]')
