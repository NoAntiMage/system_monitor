import logging


def initialize_log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%s')

    hterm = logging.StreamHandler()
    hterm.setLevel(logging.INFO)
    hterm.setFormatter(formatter)

    hfile = logging.FileHandler('./log/access.log')
    hfile.setFormatter(formatter)
    logger.addHandler(hterm)
    logger.addHandler(hfile)
    return logger


logger = initialize_log()
