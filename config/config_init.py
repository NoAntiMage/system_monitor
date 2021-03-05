from ConfigParser import SafeConfigParser
import traceback
from logger.logger import logger
import os
import os.path


class Config(SafeConfigParser):
    def __init__(self):
        SafeConfigParser.__init__(self)
        # self.config_file = './config.ini'
        self.config_file = os.path.join(os.getcwd(), 'config', 'config.ini')
        self.read(self.config_file)

    # ReturnType dict keys(main_dir)
    def disk_info(self):
        try:
            if self.has_section('disk'):
                return {'main_dir': self.get('disk', 'main_dir')}
        except Exception as e:
            logger.error(traceback.format_exc())

    # ReturnType dict keys(user, password)
    def mysql_auth(self):
        try:
            if self.has_section('mysql'):
                return {'user': self.get('mysql', 'user'), 'password': self.get('mysql', 'password')}
            else:
                raise Exception('get mysql auth failed')
        except Exception as e:
            logger.error(traceback.format_exc())

    # ReturnType dict keys(password)
    def redis_auth(self):
        try:
            if self.has_section('redis'):
                return {'password': self.get('redis', 'password')}
            else:
                raise Exception('get redis auth failed')
        except Exception as e:
            logger.error(traceback.format_exc())


config = Config()
