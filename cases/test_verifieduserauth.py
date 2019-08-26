# encoding: utf-8


"""
@version: test_webservice 1.0
@author: BigBear
@contact: zhi136@126.com
@software: PyCharm
@file: test_verifieduserauth.py
@time: 2019/8/26 13:29
"""

import unittest
import os
from scripts.handle_excel import DoExcel
from scripts.handle_mysql import DoMysql
from libs.ddt import ddt,data
from scripts.handle_config import do_config
from scripts.handle_log import do_log
from scripts.handle_webservice import DoWebService
from scripts.constants import DATAS_DIR
from scripts.handle_context import Context

http_excel_path=os.path.join(DATAS_DIR,do_config.get_value('cases excel','http_excel_name'))
sheet_name=do_config.get_value('cases excel','ver_sheet')
http_host = do_config.get_value('request info','host')

do_excel=DoExcel(http_excel_path,sheet_name)
cases = do_excel.get_cases()


@ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.do_mysql = DoMysql()
        cls.do_mysql_user = DoMysql(db_name='user_db')
        do_log.info('{:=^40s}\n'.format('测试用户实名认证接口用例开始执行'))
    @classmethod
    def tearDownClass(cls):
        cls.do_mysql.close()
        cls.do_mysql_user.close()
        do_log.info('{:=^40s}\n'.format('测试用户实名认证接口用例执行结束'))

    @data(*cases)#拆包
    def test_register(self,case):
        """
        测试用户实名认证接口
        :return:
        """
        # 处理获取的表数据
        msg=case['title']
        url = http_host + case['url']
        data = eval(Context.replace_all(str(case['data'])))
        method = case['method']
        except_result = case['expected']
        # 创建一个webservice请求对象
        dowebservice = DoWebService(url=url)
        # 发起数据请求
        request_res = dowebservice.webservice_requests(post=method,param=data)
        # 判断请求方式是否有误
        if request_res == 'PostError':
            do_log.info('{}\t执行请求方式有误！：{}\n'.format(msg, case['method']))
        # 判断是否为发送验证码接口并获取数据库验证码信息
        if 'ok' in str(request_res)  and case['method'].lower() == 'sendmcode':
            # 动态创建Context对象变量inverst_mobile_num（已发送验证码的手机号）
            setattr(Context, "invest_mobile_num", data["mobile"])
            check_sql = case['check_sql']
            if check_sql:
                check_sql = Context.replace_all(check_sql)
                mysql_data = self.do_mysql.select_mysql(sql=check_sql)
                mcode = mysql_data['Fverify_code']
                # 动态创建Context对象变量sql_mcode（验证码）
                setattr(Context,"sql_mcode",mcode)
        try:
            # 断言请求结果
            self.assertIn(except_result,str(request_res),msg=msg+'失败！')
            # 注册接口判断用户是否注册成功并写入数据库
            if 'ok' in str(request_res) and case['method'].lower() == 'userregister':
                check_sql = case['check_sql']
                setattr(Context, 'user_id', data['user_id'])
                if check_sql:
                    check_sql = Context.replace_all(check_sql)
                    mysql_data = self.do_mysql_user.select_mysql(sql=check_sql)
                    if mysql_data['Fuid'] is not None:
                        setattr(Context, 'Fuid', mysql_data['Fuid'])
                    #断言用户是否添加成功
                    self.assertIsNotNone(mysql_data,msg=msg + '数据库添加用户失败！')
            #实名认证接口判断是否认证成功并写入数据库
            if 'ok' in str(request_res) and case['method'].lower() == 'verifieduserauth':
                check_sql = case['check_sql']
                if check_sql:
                    check_sql = Context.replace_all(check_sql)
                    mysql_data = self.do_mysql_user.select_mysql(sql=check_sql)
                    #断言用户实名认证是否添加成功
                    self.assertIsNotNone(mysql_data,msg=msg + '数据库添加实名认证失败！')

            do_log.info('{}\t执行结果：{}\n'.format(msg,'Pass'))
            do_excel.write_result(case['case_id']+1,str(request_res),'Pass')
        except AssertionError as e:
            do_log.error('{}执行结果:{}\t报错信息：{}\n'.format(msg,'Fail',e))
            do_excel.write_result(case['case_id']+1,str(request_res),'Fail')
            raise e

if __name__ == '__main__':
    unittest.main()