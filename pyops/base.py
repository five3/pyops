import logging
from .libs import all_data


logger = logging.getLogger()
logger.info(f'collect data: {all_data}')


def cls_verify(cls, module, req):
    case_json = all_data['case_json']
    if module not in case_json:
        raise ValueError(f'EEEEEEEEE..module {module} not found in json..EEEEEEEEE')

    cls_info = case_json[module]
    if cls_info.get('name') != cls:
        raise ValueError(f'EEEEEEEEE..cls {cls} not found in json..EEEEEEEEE')
    elif req.config.getoption('--force_run', None):
        return cls_info
    elif cls_info.get('disable', False):
        logger.warning(f'WWWWWWW..class {cls} disabled in json..WWWWWWW')
        return None

    return cls_info


def base_verify(func_name, cls, module, req):
    cls_info = cls_verify(cls, module, req)

    if cls_info is None:
        return None

    cases = cls_info['cases']
    case = cases.get(func_name)
    if not case:
        raise ValueError(f'EEEEEEEEE..case {func_name} not found in json..EEEEEEEEE')
    elif req.config.getoption('--force_run', None):
        return case
    elif case.get('disable', False):
        logger.warning(f'WWWWWWW..case {func_name} disabled in json..WWWWWWW')
        return None

    return case


def get_func(main, key):
    if not main:
        return []

    keys = ['setup', 'teardown', 'data', 'flow', 'check', 'setup_class', 'teardown_class']
    if key not in keys:
        raise ValueError(f'function keywords only support in {keys}, current is {key}')

    func_list = main.get(key)
    if not func_list:
        return []

    ret = []
    case_func = all_data['case_func']
    for func_str in func_list:
        if func_str in case_func:
            func = case_func.get(func_str)
            if func and callable(func) and key in func.ah_type:
                ret.append(func)
            else:
                raise ValueError(f"EEEEEEEEE..function {func_str}'s ah_type error, current is {func.ah_type}, it should contain {key} ..EEEEEEEEE")
        else:
            raise ValueError(f'EEEEEEEEE..function {func_str} not found..EEEEEEEEE')

    return ret


def get_data_by_func_name(func_name, cls, module, req):
    case = base_verify(func_name, cls, module, req)
    if not case:
        return {}

    data = case.get('data', {})
    if isinstance(data, (str, bytes)):
        req.case_func = all_data['case_func']
        func = req.case_func.get(data)
        if func and callable(func) and 'data' in func.ah_type:
            data = func(req)
        else:
            raise ValueError(f'EEEEEEEEE..data function {data} not found or can not called..EEEEEEEEE')

    if not isinstance(data, dict):
        try:
            data = dict(data)
        except Exception as e:
            raise ValueError(f'EEEEEEEEE..data content convert error: {data} ..EEEEEEEEE')

    return data if data else {}


def get_flow_by_func_name(func_name, cls, module, req):
    case = base_verify(func_name, cls, module, req)
    return get_func(case, 'flow')


def get_check_by_func_name(func_name, cls, module, req):
    case = base_verify(func_name, cls, module, req)
    return get_func(case, 'check')


def get_init_by_func_name(func_name, cls, module, req):
    case = base_verify(func_name, cls, module, req)
    return get_func(case, 'setup')


def get_dest_by_func_name(func_name, cls, module, req):
    case = base_verify(func_name, cls, module, req)
    return get_func(case, 'teardown')


def get_class_init_by_name(cls, module, req):
    cls_info = cls_verify(cls, module, req)
    return get_func(cls_info, 'setup_class')


def get_class_dest_by_name(cls, module, req):
    cls_info = cls_verify(cls, module, req)
    return get_func(cls_info, 'teardown_class')


def get_class_config(config, key):
    ah_config = getattr(config, 'ah_class_config')
    if ah_config:
        return ah_config.get(key)


def set_class_config(config, key, value):
    ah_config = getattr(config, 'ah_class_config')
    ah_config[key] = value


def del_class_config(config, key):
    ah_config = getattr(config, 'ah_class_config')
    if key in ah_config:
        del ah_config[key]


def clear_class_config(config, key):
    ah_config = getattr(config, 'ah_class_config')
    if ah_config:
        ah_config = {}
