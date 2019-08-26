import logging
import time
from scripts.handle_config import do_config
from scripts.constants import LOGS_DIR

class HandleLog:
    def __init__(self):
        # 定义一个名为case的收集器
        self.case_logger = logging.getLogger(do_config.get_value('log','logger_name'))
        # 设置收集器的日志等级
        self.case_logger.setLevel(do_config.get_value('log','logger_level'))
        # 定义输出渠道
        # 控制台输出渠道
        console_handle = logging.StreamHandler()
        # 文件输出渠道
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        log_path = LOGS_DIR + '/logger_' + now + '.log'
        file_handle = logging.FileHandler(log_path, encoding='utf-8')

        # 设置输出渠道日志等级
        console_handle.setLevel(logging.ERROR)
        file_handle.setLevel(logging.INFO)
        # 定义日志格式
        simple_formatter = logging.Formatter(do_config.get_value('log','simple_formatter'))
        verbose_formatter = logging.Formatter(do_config.get_value('log','verbose_formatter'))
        # 设置日志输出格式
        console_handle.setFormatter(simple_formatter)
        file_handle.setFormatter(verbose_formatter)
        # 对接收集器与输出渠道
        self.case_logger.addHandler(console_handle)
        self.case_logger.addHandler(file_handle)
    def get_logger(self):
        return self.case_logger
do_log=HandleLog().get_logger()