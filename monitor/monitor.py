# coding: utf-8
# Description: 根据监控指标，执行监控任务
# !/usr/bin/python

from entity.sysinfo_check import Disk, Processor
from logger.logger import logger
import traceback
from request.post import warning_request
from entity.server_check import Mysql, Nginx, Redis, Zookeeper


# Description: 磁盘使用率大于阈值 或 磁盘剩余空间小于阈值 报警
# ReturnType Disk
def disk_check():
    try:
        disk = Disk()
        logger.info(disk)
        # todo config_parser
        # todo warning_request()

        assert type(disk.percent) == int
        assert type(disk.avail) == int

        if disk.percent > 85:
            warning_request('disk percent')
        elif disk.avail < 10 * 1024 * 1024:
            warning_request('disk avail')
        else:
            pass
        return disk
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        logger.info('-' * 20 + '\n')


# Description: cpu_metric 定义为 负载1分钟、5分钟、15分钟平均值
# 平均负载大于1.5 报警， cpu使用率大于 90 报警
def cpu_check():
    try:
        cpu = Processor()
        # print(cpu)
        cpu_metric = (cpu.upload['1m'] + cpu.upload['5m'] + cpu.upload['15m']) / 3
        average = cpu_metric / cpu.cpu_count
        assert type(average) == float

        if 1 < average <= 1.5:
            logger.warning('cpu is overload! upload: ' + str(cpu))
        elif average > 1.5:
            logger.error('cpu is highly overload! please check processes. upload: ' + str(cpu))
        elif cpu.percent > 90:
            logger.warning('cpu usage is too high! cpu usage: ' + str(cpu.percent))
        else:
            logger.info('cpu status: ' + str(cpu))
        # print('cpu_metric is : ' + str(cpu_metric))
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        logger.info('-' * 20 + '\n')


# svc ParamType AppCheck
class Monitor(object):
    def __init__(self, svc):
        self.svc = svc

    def server_status_check(self):
        status = self.svc.request_status & self.svc.listen_status
        if status is True:
            logger.info('{} status : OK'.format(self.svc.name))
        else:
            warning_request(self.svc.name)
            logger.warning('{} status : FAIL'.format(self.svc.name))
        logger.info('-' * 20 + '\n')


def mysql_check():
    mysql = Mysql()
    m = Monitor(mysql)
    m.server_status_check()


def nginx_check():
    nginx = Nginx()
    m = Monitor(nginx)
    m.server_status_check()


def redis_check():
    redis = Redis()
    m = Monitor(redis)
    m.server_status_check()


def zookeeper_check():
    zk = Zookeeper()
    m = Monitor(zk)
    m.server_status_check()


