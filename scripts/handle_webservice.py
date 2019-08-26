# encoding: utf-8


"""
@version: test_webservice 1.0
@author: BigBear
@contact: zhi136@126.com
@software: PyCharm
@file: handle_webservice.py
@time: 2019/8/22 15:43
"""
from suds.client import Client
from scripts.handle_log import do_log


class DoWebService:
    def __init__(self,url):
        self.client = Client(url=url)

    def webservice_requests(self,post,param):
        if post.lower() == 'sendmcode':
            return self.webservice_sendmcode(param=param)
        elif post.lower() == 'userregister':
            return self.webservice_userregister(param=param)
        elif post.lower() == 'verifieduserauth':
            return self.webservice_verifieduserauth(param=param)
        else:
            return 'PostError'

    #发送短信验证码接口请求
    def webservice_sendmcode(self,param):
        try:
            result = self.client.service.sendMCode(param)
            return dict(result)
        except Exception as e:
            do_log.error('发送短信验证码接口请求出现异常:{}\n'.format(e))
            return e



    #注册接口请求
    def webservice_userregister(self,param):
        try:
            result = self.client.service.userRegister(param)
            return dict(result)
        except Exception as e:
            do_log.error('注册接口请求出现异常:{}\n'.format(e))
            return e



    #实名认证接口请求
    def webservice_verifieduserauth(self, param):
        try:
            result = self.client.service.verifyUserAuth(param)
            return dict(result)
        except Exception as e:
            do_log.error('实名认证接口请求出现异常:{}\n'.format(e))
            return e
            # raise e



if __name__ == '__main__':
    # url = r'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
    url = r'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    param = {'client_ip':'172.16.3.25','tmpl_id':'1','mobile':'13170865816'}

    result = DoWebService(url).webservice_sendmcode(param)
    print(result)