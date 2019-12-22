![关注二维码](https://www.testqa.cn/static/banner.png)

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
pip install py-ops
```
或者使用下面命令安装最细版：
```bash
pip install git+https://github.com/five3/pyops.git
```

## 快速开始
使用该框架非常的方便，基本没有学习成本。首先新建一个目录作为自动化项目的根目录，然后再新建一个名为`ah_ext`的python包目录，并在`__init__.py`文件中编写如下内容。
```python
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
```

在该目录下新建一个`demo.json`文件，内容如下：
```bash
{
	"name": "TestDemo",
	"desc": ".....background......",
	"tag": "smoking_test",
	"setup_class": [],
	"teardown_class": [],
	"cases": {
		"test_add": {
			"desc": "",
			"tags": [],
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
在项目根目录执行如下命令运行测试：
```bash
pyops run
```
该命令默认会执行当前目录先全部的json用例文件，如果你希望只执行部分的json用例，则可以指定特定的文件名：
```bash
pyops run demo.jsom demo2.json
```
另外，在执行完该命令后会在当前目录生成一个对应名称的py文件，如：demo.py。这个执行测试流程中的产物，也是执行测试的真正入口点。如果你希望单独生成一个py用例文件，可以使用下面的命令：
```bash
pyops make demo.json
```

## 框架设计结构
