import datetime


def get_sys_date():
    ISO_time_format = "%Y%m%d"
    current_time = datetime.datetime.now().strftime(ISO_time_format)
    return current_time

