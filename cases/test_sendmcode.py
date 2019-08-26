# encoding: utf-8


"""
@version: test_webservice 1.0
@author: BigBear
@contact: zhi136@126.com
@software: PyCharm
@file: test_sendmcode.py
@time: 2019/8/24 11:38
"""


import unittest
import os
from scripts.handle_excel import DoExcel
from libs.ddt import ddt,data
from scripts.handle_config import do_config
from scripts.handle_log import do_log
from scripts.handle_webservice import DoWebService
from scripts.constants import DATAS_DIR
from scripts.handle_context import Context

http_excel_path=os.path.join(DATAS_DIR,do_config.get_value('cases excel','http_excel_name'))
sheet_name=do_config.get_value('cases excel','send_sheet')
http_host = do_config.get_value('request info','host')


do_excel=DoExcel(http_excel_path,sheet_name)
cases = do_excel.get_cases()


@ddt
class TestSendMCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        do_log.info('{:=^40s}\n'.format('测试发送短信验证码接口用例开始执行'))
    @classmethod
    def tearDownClass(cls):
        do_log.info('{:=^40s}\n'.format('测试发送短信验证码接口用例执行结束'))

    @data(*cases)#拆包
    def test_sendmcode(self,case):
        """
        测试发送短信验证码接口
        :return:
        """
        # 处理获取的表数据
        msg=case['title']
        url = http_host + case['url']
        data = eval(Context.new_mobile_tel_replace(str(case['data'])))
        method = case['method']
        # 创建一个webservice请求对象
        dowebservice = DoWebService(url=url)
        # 发起数据请求
        request_res = dowebservice.webservice_requests(post=method,param=data)
        # 判断请求方式是否有误
        if request_res == 'PostError':
            do_log.info('{}\t执行请求方式有误！：{}\n'.format(msg, case['method']))
        except_result = case['expected']

        try:
            # 断言请求结果
            self.assertIn(except_result,str(request_res),msg=msg+'失败！')
            do_log.info('{}\t执行结果：{}\n'.format(msg,'Pass'))
            do_excel.write_result(case['case_id']+1,str(request_res),'Pass')
        except AssertionError as e:
            do_log.error('{}执行结果:{}\t报错信息：{}\n'.format(msg,'Fail',e))
            do_excel.write_result(case['case_id']+1,str(request_res),'Fail')
            raise e

if __name__ == '__main__':
    unittest.main()