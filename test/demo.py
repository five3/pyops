# -*- coding: utf-8 -*- 
import pytest
import logging
import subprocess
from pyops.main import *

logger = logging.getLogger()

# 打全局标签，比如功能模块标签
pytestmark = pytest.mark.clues


class TestDemo:
    def test_001(self, class_init, class_dest, init, dest, test_data, test_flow, test_check):
        pass

    def test_002(self, class_init, class_dest, init, dest, test_data, test_flow, test_check):
        pass


if __name__ == "__main__":
    subprocess.call(['pytest', "-s", "demo.py", "--pytest_report", "report.html"])
