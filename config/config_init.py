from ConfigParser import SafeConfigParser
import traceback
import os
import os.path


class Config(SafeConfigParser):
    def __init__(self):
        SafeConfigParser.__init__(self)
        # self.config_file = './config.ini'
        config_path = os.path.dirname(__file__)
        self.config_file = os.path.join(config_path, 'config.ini')
        try:
            self.read(self.config_file)
        except Exception:
            traceback.format_exc()


config = Config()
