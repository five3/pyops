import os
import json
import jinja2
import optparse
import subprocess
from logging.config import dictConfig

__version__ = '0.1.3'


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.getcwd(), './std.log'),
            'level': 'DEBUG',
            'formatter': 'default',
            'encoding': 'utf-8'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
})


__TMPL__ = """# -*- coding: utf-8 -*- 
import pytest
import logging
from pyops.main import *

logger = logging.getLogger()

# 打全局标签，比如功能模块标签
pytestmark = pytest.mark.{{ tag }}


class {{ class }}:{% for case in cases %}
    def {{ case }}(self, class_init, class_dest, init, dest, test_data, test_flow, test_check):
        pass
{% endfor %}

if __name__ == "__main__":
    pytest.main(["-s", "{{ module }}.py", "--pytest_report", "report.html"])

"""

__INI_TMPL__ = """[pytest]
markers = {% for tag in tags %}
    {{ tag }}
{% endfor %}
"""

__JSON_TMPL__ = """{
    "name": "TestDemo",
    "desc": ".....background......",
    "tag": "smoking_test",
    "setup_class": [],
    "teardown_class": [],
    "setup": [],
    "teardown": [],
    "cases": {
        "test_add": {
            "desc": "",
            "tags": [],
            "data": {
                "x": 2,
                "y": 3,
                "expect": 5
            },
            "flow": ["调用add"],
            "check": ["检查add"]
        }
    }
}
"""

__INIT_TMPL__ = '''import logging
from pyops.decorator import (make_check, make_flow, alias)

logger = logging.getLogger()

def add(x, y):
    print('add')
    return x + y

@alias('调用add')
@make_flow
def call_add(data):
    """
        data: 即json配置文件中的case节点下对应data字典对象
    """
    data['actual'] = add(data['x'], data['y'])

@alias('检查add')
@make_check
def check_add(data):
    """
        data: 即json配置文件中的case节点下对应data字典对象
    """
    return data['actual'] == data['expect']
'''


def run(args):
    case_files = make(args)
    args = ["pytest"] + case_files + ["-s", "-v" "--pytest_report", "report.html"]
    subprocess.call(args)


def force_run(args):
    case_files = make(args)
    args = ["pytest"] + case_files + ["-s", "-v", "--force_run", "--pytest_report", "report.html"]
    subprocess.call(args)


def make(args):
    files = args[1:] if len(args) > 1 else get_files()
    all_tags = []
    case_files = []

    for file in files:
        with open(os.path.join(os.getcwd(), file), 'r', encoding='utf8') as fr:
            json_data = json.load(fr)
            all_tags.append(json_data['tag'])

            content = gen_template_file({
                "module": file.replace(".json", ""),
                "class": json_data['name'],
                "tag": json_data['tag'],
                "cases": [case for case in json_data['cases']]
            }, __TMPL__)

            case_file = file.replace('.json', '.py')
            case_files.append(case_file)
            with open(os.path.join(os.getcwd(), case_file), 'w', encoding='utf8') as fw:
                fw.write(content)

    with open(os.path.join(os.getcwd(), 'pytest.ini'), 'w', encoding='utf8') as fw:
        content = gen_template_file({
            'tags': set(all_tags)
        }, __INI_TMPL__)
        fw.write(content)

    return case_files


def start_project(args):
    project_name = args[1]

    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, 'ah_ext'))

    with open(os.path.join(project_name, 'ah_ext', '__init__.py'), 'w', encoding='utf-8') as f:
        f.write(__INIT_TMPL__)

    with open(os.path.join(project_name, 'demo.json'), 'w', encoding='utf-8') as f:
        f.write(__JSON_TMPL__)


def get_files():
    sub_files = os.listdir(os.getcwd())
    return [sub_file for sub_file in sub_files if sub_file.endswith('json')]


def gen_template_file(data, temp_str):
    template = jinja2.Template(temp_str)
    return template.render(data)


def main():
    usage = "USAGE: pyops run|make|forcerun|startproject projectname"
    op = optparse.OptionParser(usage=usage)
    option, args = op.parse_args()

    if len(args) < 1:
        op.print_help()
        exit(1)

    action = args[0]
    if action == 'run':
        run(args)
    elif action == 'make':
        make(args)
    elif action == 'forcerun':
        force_run(args)
    elif action == 'startproject':
        if len(args) < 2:
            print('[ERROR] startproject common must have a arg')
            op.print_help()
        else:
            start_project(args)
    else:
        op.print_help()


if __name__ == '__main__':
    main()
