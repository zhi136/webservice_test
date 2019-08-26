import pymysql
import random
from scripts.handle_config import do_config

start_mobile_dict = do_config.get_eval_data('mobile phone', 'start_mobile')
host = do_config.get_value('mysql','host')
user=do_config.get_value('mysql','user')
password=do_config.get_value('mysql','password')
db_hand=do_config.get_value('mysql','db_hand')
end_mobile = do_config.get_value('mobile phone','end_mobile')
db = db_hand + end_mobile[1:3]
table_name_hand=do_config.get_value('mysql','table_name_hand')
table_name =table_name_hand + end_mobile[0]
port=do_config.get_int('mysql','port')
# print(host,type(host),user,type(user),password,type(password),db,type(db),port,type(port))

class DoMysql:
    def __init__(self,db_name=None):
        self.db=db_name
        if self.db == None:
            self.conn = pymysql.connect(host=host,
                                   user=user,
                                   password=password,
                                   db=db, port=port,
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor)
        else:
            self.conn = pymysql.connect(host=host,
                                        user=user,
                                        password=password,
                                        db=self.db, port=port,
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def select_mysql(self,sql,args=None,is_more=False):
        self.cursor.execute(sql,args=args)
        self.conn.commit()
        if is_more == True:
            return self.cursor.fetchall()
        elif is_more == False:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    #随机生成一个手机号
    @staticmethod
    def random_mobile_phone():
        start_mobile = str(random.choice(start_mobile_dict))
        new_mobile = start_mobile + ''.join(random.sample('0123456789', 5)) + end_mobile
        return new_mobile

    #查询手机号对应数据库记录
    @staticmethod
    def select_mobile_phone(mobile):
        do_mysql = DoMysql()
        sql = 'select * from '+ table_name +' where Fmobile_no=%s'
        result = do_mysql.select_mysql(sql, args=(mobile,))
        do_mysql.close()
        return result

    #创建一个未注册过的手机号
    @staticmethod
    def create_new_mobile():
        while True:
            new_mobile = DoMysql.random_mobile_phone()
            result = DoMysql.select_mobile_phone(new_mobile)
            if result == None:
                break
        return new_mobile


if __name__ == '__main__':

    # sql2= 'select * from `t_mvcode_info_8` where Fmobile_no=%s'
    # result2 = DoMysql().select_mysql(sql2, args=("13170865816",))
    result2 = DoMysql().select_mobile_phone('13170865816')
    print(result2['Fverify_code'])