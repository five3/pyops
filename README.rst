py-ops: 一款面向编程的Python关键字测试框架™
============================================

.. image:: https://raw.githubusercontent.com/five3/pyops/master/images/testqa.png

☤ 说明
------

这是一款基于``pytest``封装，同时支持``关键字``和``BDD``，测试数据分离，面向编程，轻量级的，对上层自动化应用友好的基础测试框架。

其主要核心功能：

- 支持关键字定义
- 支持关键字组装
- 测试数据透传

该框架的主要特点：

- 基于``pytest``框架开发，支持原生插件
- 同时具备``关键字``和``BDD``框架的特点
- 无二次学习成本(Python|json)
- 天然支持``测试数据分离``与传递
- 对上层应用提供友好的封装接口
- 支持脚本``Debug``调试
- 代码量少(7个文件500行代码)


☤ 环境安装
----------

.. code:: bash

    pip install py-ops


或者使用下面命令安装最新版：

.. code:: bash

    pip install git+https://github.com/five3/pyops.git


☤ 快速开始
----------

使用该框架非常的方便，基本没有学习成本。安装完成之后，在任意目录执行如下命令创建一个测试项目：

.. code:: bash

    pyops startproject test1


命令执行完成之后，会在当前目录创建一个[test1]目录，具体的目录结构如下：

.. code:: bash

    |- test1
        |-- ah_ext
            |-- __init__.py
        |-- demo.json


接着在测试项目根目录(test1)执行如下命令运行测试：

.. code:: bash

    pyops run


该命令默认会执行当前目录先全部的json用例文件，如果你希望只执行部分的json用例，则可以指定特定的文件名：

.. code:: bash

    pyops run demo.jsom demo2.json


在执行完run命令后会在当前目录生成多个文件，具体的文件如下：

.. code:: bash

    |- test1
        |-- ah_ext
            |-- __init__.py
        |-- demo.json
        |-- demo.py
        |-- pytest.ini
        |-- report.html
        |-- std.log


其中demo.py是由json文件生成的同名用例文件，这个是执行测试流程中的产物，也是执行测试的真正入口点。
report.html是测试报告，std.log则是测试的详细日志，pytest.ini自动生成的pytest配置文件。

如果你希望单独生成一个py用例文件，可以使用下面的命令：

.. code:: bash

    pyops make demo.json


json文件中还可以对case配置disable字段，为true时则不会执行，不填时默认为false。
如果希望强制运行disable为true的用例，可以使用forcerun命令。

.. code:: bash

    pyops forcerun


当然，你也可以通过原生的pytest命令来执行，前提是已经通过make、run命令生成了py文件。比如：

.. code:: bash

    pytest demo.py::test_cls_name::test_case_name -s -v --force_run --pytest_report report.html


其中-s、-v是pytest原生的参数，--force_run是pyops插件参数，--pytest_report则是PyTestReport插件参数。

☤ 框架设计结构
--------------
.. image:: https://raw.githubusercontent.com/five3/pyops/master/images/apic.png


☤ 自动生成用例说明
------------------
自动生成的demo.json测试用例内容如下：

.. code:: bash

    {
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


自动生成的``ah_ext.__init__.py``文件内容如下：

.. code:: python

    import logging
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