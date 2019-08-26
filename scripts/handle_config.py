import os
from configparser import ConfigParser
from scripts.constants import CONFIGS_DIR

class HandleConfig:
    """

    """
    def __init__(self,filename):
        self.filename=filename
        self.config=ConfigParser()
        self.config.read(self.filename,encoding='utf-8')
    def get_value(self,section,option):
        return self.config.get(section,option)
    def get_int(self,section,option):
        return self.config.getint(section,option)
    def get_float(self,section,option):
        return self.config.getfloat(section,option)
    def get_boolean(self,section,option):
        return self.config.getboolean(section,option)
    def get_eval_data(self,section,option):
        return eval(self.get_value(section,option))

    @staticmethod
    def write_config(datas,filename):
        if isinstance(datas,dict):
            for value in datas.values():
                if not isinstance(value,dict):
                    return
                else:
                    config=ConfigParser()
                    for key in datas:
                        config[key]=datas[key]
                    with open(filename,'w') as file:
                        config.write(file)

config_path = os.path.join(CONFIGS_DIR,'testcase.conf')
# do_config = HandleConfig('./configs/testcase.configs')
do_config = HandleConfig(config_path)