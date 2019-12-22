# 说明
这是一款基于`pytest`封装，同时支持`关键字`和`BDD`，测试数据分离，面向编程，轻量级的，对上层自动化应用友好的基础测试框架。

其主要核心功能：
1. 支持关键字定义
1. 支持关键字组装
1. 测试数据透传

该框架的主要特点：
1. 基于`pytest`框架开发，支持原生插件
1. 同时具备`关键字`和`BDD`框架的特点
1. 无二次学习成本(Python|json)
1. 天然支持`测试数据分离`与传递
1. 对上层应用提供友好的封装接口
1. 支持脚本`Debug`调试
1. 代码量少(7个文件500行代码)

## 环境安装
```bash
git clone https://git.corpautohome.com/ad-qa/ah-api-core.git
cd ah-api-core
pip install -r requirements.txt
python setup.py install
```
或者
```bash
pip install git+https://git.corpautohome.com/ad-qa/ah-api-core.git
```

## 快速开始
使用该框架非常的方便，基本没有学习成本。首先新建一个目录作为自动化项目的根目录，然后再新建一个名为`ah_ext`的python包目录，并在`__init__.py`文件中编写如下内容。
```python
import logging
from ahAPICore.decorator import (make_check, make_flow, alias)

logger = logging.getLogger()

def add(x, y):
    print('add')
    return x + y

@alias('调用add')
@make_flow
def call_add(data):
    data['actual'] = add(data['x'], data['y'])

@alias('检查add')
@make_check
def check_add(data):
    return data['actual'] == data['expect']
```

在该目录下新建一个`demo.json`文件，内容如下：
```bash
{
	"name": "TestDemo",
	"desc": ".....background......",
	"tag": ["smoking_test"],
	"setup_class": [],
	"teardown_class": [],
	"cases": {
		"test_add": {
			"desc": "",
			"tag": [],
			"setup": [],
			"teardown": [],
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
```
同时创建一个名为`demo.py`的python文件，其内容如下（该文件后期可以省略，有框架自动生成）：
```python
import pytest
import logging
from ahAPICore.main import *

logger = logging.getLogger()

class TestDemo:
    def test_add(self, class_init, class_dest, init, dest, test_data, test_flow, test_check):
        logger.info(f'......do testing for test_001.......')


if __name__ == "__main__":
    pytest.main(["-s", "demo.py", "--force_run", "--pytest_report", "report.html"])
```
在命令行直接执行该文件，即可运行测试并在当前目录输出测试报告和日志文件。

## 框架设计结构
![](http://pcma.corpautohome.com/docs/_images/apic.png)