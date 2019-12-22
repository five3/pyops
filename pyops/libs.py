import os
import sys
import json
import logging
import traceback
from inspect import isfunction
from importlib import import_module

logger = logging.getLogger()

JSON_PATH = [os.getcwd()]

FUNC_PATH = [os.path.join(os.path.dirname(__file__), 'ext')]
func_path = [os.environ.get("AH_EXT"), os.path.join(os.getcwd(), 'ah_ext')]
for fp in func_path:
    if fp and os.path.isdir(fp):
        FUNC_PATH.append(fp)


def collect_func(case_py, package=None):
    all_func = {}
    for m in case_py:
        import_str = f'{m}' if package is None else f'{package}.{m}'
        import_str = import_str[:-9] if import_str.endswith('__init__') else import_str
        case_module = import_module(import_str)

        all_mem = dir(case_module)
        for mem in all_mem:
            if mem.startswith('__') or mem.endswith('__'):
                continue

            func = getattr(case_module, mem)
            if isfunction(func) and hasattr(func, 'ah_type') \
                and set(func.ah_type) & {'data', 'flow', 'check', 'setup', 'teardown', 'setup_class', 'teardown_class'}:
                all_func[f'{import_str}.{mem}'] = func
                if hasattr(func, 'alias'):
                    if func.alias in all_func:
                        raise KeyError(f'The alias [{func.alias}] already exist when set for function [{case_module.__name__}.{func.__name__}]')
                    all_func[func.alias] = func

    return all_func


def collect_module(target_dir=None):
    case_func = {}
    target_dir = target_dir if target_dir else FUNC_PATH
    for p in target_dir:
        case_module = []
        sub_list = os.listdir(p)
        for sub in sub_list:
            if sub.endswith('.py'):
                case_module.append(sub[:-3])

        if '__init__.py' in sub_list:  # is a package
            par_dir = os.path.dirname(p)
            if par_dir not in sys.path:
                sys.path.insert(0, par_dir)
            case_func.update(collect_func(case_module, package=os.path.basename(p)))
        else:  # is not a package
            if p not in sys.path:
                sys.path.insert(0, p)
            case_func.update(collect_func(case_module))

    return case_func


def collect_json(target_dir=None):
    case_json = {}
    target_dir = target_dir if target_dir else JSON_PATH

    for p in target_dir:
        sub_list = os.listdir(p)
        for sub in sub_list:
            if sub.endswith('.json'):
                with open(os.path.join(p, sub), 'r', encoding='utf8') as f:
                    case_json[sub[:-5]] = json.load(f)

    if not case_json:
        raise ValueError(f'EEEEEEEEE..there is no json file found..EEEEEEEEE')

    return case_json


def collect_all():
    return {
        "case_json": collect_json(),
        "case_func": collect_module()
    }


try:
    all_data = collect_all()
except:
    logging.error('function collect_all data except')
    traceback.print_exc()
    exit(1)
    all_data = None

