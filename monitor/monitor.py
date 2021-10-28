# coding: utf-8
# Description: 根据监控指标，执行监控任务
# !/usr/bin/python

from config.config_init import config
from entity.sysinfo_check import Disk, Processor, Memory, InputOutput
from logger.logger import logger
import traceback
from request.post import warning_request
from entity.server_check import Mysql, Nginx, Redis, Zookeeper
from util.unitutil import get_power_index
from template.warning_msg import *


# todo warning_request()

# Description: 磁盘使用率大于阈值 或 磁盘剩余空间小于阈值 报警
# ReturnType Disk
def disk_check():
    try:
        disk = Disk()
        logger.info(disk)
        percent_metric = float(config.get("disk", "percent"))
        available_metric = float(config.get("disk", "available_G"))

        assert type(disk.percent) == int
        assert type(disk.avail) == int
        assert type(available_metric) == float

        if disk.percent > percent_metric:
            logger.warning(disk_percent_warning + 'disk usage: {}%\n'.format(disk.percent))
        if disk.avail < available_metric * 1024 * 1024:
            unit, index = get_power_index()
            logger.warning(disk_available_warning + 'available disk: {} {}b\n'.format(disk.avail/(1024**index), unit))
        return disk
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: cpu_metric 定义为 负载1分钟、5分钟、15分钟平均值
# 平均负载大于阈值 报警， cpu使用率大于阈值 报警
def cpu_check():
    try:
        cpu = Processor()
        cpu_metric = (cpu.upload['1m'] + cpu.upload['5m']) / 2.00
        average = cpu_metric / cpu.cpu_count
        assert type(average) == float

        thread_per_process = float(config.get("cpu", "thread_per_cpu"))
        percent_metric = float(config.get("cpu", "percent"))

        if average > thread_per_process:
            logger.warning(cpu_overload_warning + 'upload: {}\n'.format(average))
        if cpu.percent > percent_metric:
            logger.warning(cpu_usage_warning + 'cpu usage: {:.2f} %\n'.format(cpu.percent))

        logger.info(cpu)
        # print('cpu_metric is : ' + str(cpu_metric))
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: 应用程序内存使用率大于 阈值 报警
def memory_check():
    try:
        mem = Memory()

        percent_metric = float(config.get("memory", "percent"))
        if mem.percent > percent_metric:
            logger.warning(memory_usage_warning + 'memory usage: {:.2f} %\n'.format(mem.percent))
        logger.info(mem)
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: 读写耗时超过阈值 报警，读写队列长度超过阈值 报警
def io_check():
    try:
        io = InputOutput()
        await_metric = float(config.get("input-output", "await"))
        util_metric = float(config.get("input-output", "util"))
        if io.await > await_metric:
            logger.warning(io_delay_warning + 'time: {} ms\n'.format(io.await))
        if io.util > util_metric:
            logger.warning(io_queue_warning + 'io queue usage : {} %\n'.format(io.util))

        logger.info(io)
    except Exception as e:
        logger.error(traceback.format_exc())


# svc ParamType AppCheck
class Monitor(object):
    def __init__(self, svc):
        self.svc = svc

    def server_status_check(self):
        status = self.svc.request_status & self.svc.connect_status & self.svc.listen_status
        if status is True:
            logger.info('{} status : OK\n'.format(self.svc.name))
        else:
            warning_request(self.svc.name, 0)
            logger.warning('{} status : FAIL\n'.format(self.svc.name))


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


