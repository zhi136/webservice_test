import os

# #获取当前文件路径
# present_path =  os.path.abspath(__file__)
# #获取当前文件上一级目录
# up_present_path = os.path.dirname(present_path)
# #获取项目目录（上上一级目录）
# project_path =  os.path.dirname(up_present_path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#配置文件路径
CONFIGS_DIR = os.path.join(BASE_DIR,'configs')
#报告文件路径
REPORTS_DIR = os.path.join(BASE_DIR,'reports')
#日志文件路径
LOGS_DIR = os.path.join(BASE_DIR,'logs')
#测试用例路径
CASES_DIR = os.path.join(BASE_DIR,'cases')
#数据存放路径
DATAS_DIR = os.path.join(BASE_DIR,'datas')
#执行脚本文件路径
SCRIPTS_DIR = os.path.join(BASE_DIR,'scripts')
pass