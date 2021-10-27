import logging
import os
from util.timeutil import get_sys_date


def initialize_log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    hterm = logging.StreamHandler()
    hterm.setLevel(logging.INFO)
    hterm.setFormatter(formatter)

    current_time = get_sys_date()
    project_path = os.path.dirname(os.path.dirname(__file__))
    hfile = logging.FileHandler('{}/log/access-{}.log'.format(project_path, current_time), mode='a')
    hfile.setFormatter(formatter)
    logger.addHandler(hterm)
    logger.addHandler(hfile)
    return logger


logger = initialize_log()
