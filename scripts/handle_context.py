import re
import os
import random
from scripts.handle_config import do_config
from scripts.handle_mysql import DoMysql
from scripts.random_scard_num import getRandomIdCard
# from scripts.handle_excel import DoExcel
# from scripts.constants import DATAS_DIR


class Context:
    """
    替换参数
    """
    new_mobile_tel = do_config.get_eval_data('mobile phone', 'new_mobile_tel')
    invest_mobile_tel = do_config.get_eval_data('mobile phone', 'invest_mobile_tel')
    mcode = do_config.get_eval_data('mobile phone', 'mcode')
    username = do_config.get_eval_data('mobile phone', 'username')
    invest_user_name = do_config.get_eval_data('mobile phone', 'invest_user_name')
    fuid = do_config.get_eval_data('mobile phone', 'fuid')
    cre_id = do_config.get_eval_data('mobile phone', 'cre_id')
    start_scard = do_config.get_eval_data('mobile phone', 'start_scard')
    # http_excel_path = os.path.join(DATAS_DIR, do_config.get_value('cases excel', 'http_excel_name'))
    # mobile_sheet = do_config.get_value('mobile phone', 'mobile_sheet')
    @classmethod
    def new_mobile_tel_replace(cls,data):
        if re.search(cls.new_mobile_tel,data):
            do_mysql = DoMysql()
            #获取数据库中未注册过的手机号
            new_telephone_num = do_mysql.create_new_mobile()
            data = re.sub(cls.new_mobile_tel,new_telephone_num,data)
            do_mysql.close()
        return data

    @classmethod
    def invest_tel_replace(cls, data):
        if re.search(cls.invest_mobile_tel, data):
            invest_telephone_num = str(getattr(Context, "invest_mobile_num"))
            data = re.sub(cls.invest_mobile_tel, invest_telephone_num, data)
        return data

    @classmethod
    def username_replace(cls, data):
        if re.search(cls.username, data):
            username = '大熊测试'+str(random.randint(1,100))+str(random.randint(1,1000))
            data = re.sub(cls.username, username, data)
        return data

    @classmethod
    def mcode_replace(cls, data):
        if re.search(cls.mcode, data):
            mcode = str(getattr(Context, "sql_mcode"))
            data = re.sub(cls.mcode, mcode, data)
        return data

    @classmethod
    def invest_user_name_replace(cls, data):
        if re.search(cls.invest_user_name, data):
            user_id = str(getattr(Context, "user_id"))
            data = re.sub(cls.invest_user_name,user_id, data)
        return data

    @classmethod
    def fuid_replace(cls, data):
        if re.search(cls.fuid, data):
            fuid = str(getattr(Context, "Fuid"))
            data = re.sub(cls.fuid, fuid, data)
        return data

    @classmethod
    def cre_id_replace(cls, data):
        if re.search(cls.cre_id, data):
            cre_id = getRandomIdCard()
            data = re.sub(cls.cre_id, cre_id, data)
        return data

    @classmethod
    def replace_all(cls,data):
        data = cls.new_mobile_tel_replace(data)
        data = cls.invest_tel_replace(data)
        data = cls.mcode_replace(data)
        data = cls.username_replace(data)
        data = cls.invest_user_name_replace(data)
        data = cls.fuid_replace(data)
        data = cls.cre_id_replace(data)
        return data

if __name__ == '__main__':
    data ='{"client_ip": "", "tmpl_id": "1", "mobile": "${new_mobile_phone}"}'
    data1 = eval(Context.new_mobile_tel_replace(data))
    print(data1,type(data1))

