#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
import pyops

# python setup.py sdist
# python setup.py bdist
# python setup.py bdist_egg
# python setup.py bdist_wheel
# twine upload dist/*0.1.4*


def read(f):
    return open(f, encoding='utf-8').read()


setup(
    name="py-ops",
    version=pyops.__version__,
    keywords=("python unit testing", "auto testing", "keyword base framework", "BDD testing"),
    description="a python base auto testing framework that programming oriented with Structured Language.",
    long_description=read('README.rst'),
    license="MIT V3",

    url="https://github.com/five3/pyops.git",
    author="Xiaowu Chen",
    author_email="five3@163.com",

    package_dir={'pyops': 'pyops'},         # 指定哪些包的文件被映射到哪个源码包
    packages=find_packages(),       # 需要打包的目录。如果多个的话，可以使用find_packages()自动发现
    include_package_data=True,
    package_data={'pyops': ['*']},
    py_modules=[],          # 需要打包的python文件列表
    data_files=[            # 打包时需要打包的数据文件
    ],
    platforms="any",
    install_requires=[      # 需要安装的依赖包
        'pytest>=5.0.1',
        'pytestreport>=0.1.9.3',
        "Jinja2>=2.10.1"
    ],
    scripts=[],             # 安装时复制到PATH路径的脚本文件
    entry_points={
        'console_scripts': [    # 配置生成命令行工具及入口
            'pyops = pyops:main'
        ],
        "pytest11": ["pyops = pyops.pytestplus"]
    },
    classifiers=[           # 程序的所属分类列表
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest"
    ],
    zip_safe=False
)
