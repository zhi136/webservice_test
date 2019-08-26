#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 21:41
# @Author  : DecBear
# @File    : run.py
# @Software: PyCharm Community Edition

import time
import unittest
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.constants import REPORTS_DIR,CASES_DIR


#创建加载器并指定测试用例文件目录为当前PY文件所在目录
test_suite=unittest.defaultTestLoader.discover(CASES_DIR)

#获取时间戳
now=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))

#定义报告名称
report_name=REPORTS_DIR+'/report_'+str(now)+'.html'

#创建HTML运行器
with open(report_name , mode='wb') as report_to_file:
    html_runner=HTMLTestRunner(stream=report_to_file,
                                title='这是测试报告标题',
                                verbosity=2,#verbosity是为了指定报告的详细程度，0，1，2（0是最不详细，2是最详细）
                                description='这里填写报告的描述信息的',
                                tester='DecBear_test'#测试者名称
                                )
    html_runner.run(test_suite)#执行测试用例
