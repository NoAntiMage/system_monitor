# coding: utf-8
# Description: 根据监控指标，执行监控任务
# !/usr/bin/python

from config.config_init import config
from entity.sysinfo_check import Disk, Processor, Memory, InputOutput
from logger.logger import logger
import traceback
from request.post import warning_request
from entity.server_check import Mysql, Nginx, Redis, Zookeeper


# todo warning_request()

# Description: 磁盘使用率大于阈值 或 磁盘剩余空间小于阈值 报警
# ReturnType Disk
def disk_check():
    try:
        disk = Disk()
        logger.info(disk)
        percent_metric = int(config.get("disk", "percent"))
        available_metric = int(config.get("disk", "available"))

        assert type(disk.percent) == int
        assert type(disk.avail) == int
        assert type(available_metric) == int

        if disk.percent > percent_metric:
            logger.warning('disk percent is too high!\ndisk usage:' + disk.percent)
        elif disk.avail < int(available_metric) * 1024 * 1024:
            logger.warning('disk avail is too low!\navailable disk:' + disk.avail)
        else:
            pass
        return disk
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: cpu_metric 定义为 负载1分钟、5分钟、15分钟平均值
# 平均负载大于阈值 报警， cpu使用率大于阈值 报警
def cpu_check():
    try:
        cpu = Processor()
        cpu_metric = (cpu.upload['1m'] + cpu.upload['5m'] + cpu.upload['15m']) / 3
        average = cpu_metric / cpu.cpu_count
        assert type(average) == float

        thread_per_process = int(config.get("cpu", "thread_per_cpu"))
        percent_metric = int(config.get("cpu", "percent"))

        if average > thread_per_process:
            logger.warning('cpu is overload! upload: ' + str(cpu))
        if cpu.percent > percent_metric:
            logger.warning('cpu usage is too high!\ncpu usage: ' + str(cpu.percent))

        logger.info(cpu)
        # print('cpu_metric is : ' + str(cpu_metric))
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: 应用程序内存使用率大于 阈值 报警
def memory_check():
    try:
        mem = Memory()

        percent_metric = int(config.get("memory", "percent"))
        if mem.percent > percent_metric:
            logger.warning('high memory usage!\nmemory usage: {} %'.format(mem.percent))
        logger.info(mem)
    except Exception as e:
        logger.error(traceback.format_exc())


# Description: 读写耗时超过阈值 报警，读写队列长度超过阈值 报警
def io_check():
    try:
        io = InputOutput()
        if io.await > config.get("input-output", "await"):
            logger.warning("per io spend too much time: {} ms".format(io.await))
        if io.util > config.get("input-output", "util"):
            logger.warning("disk io is overload! io queue usage : {} %".format(io.util))

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
            logger.info('{} status : OK'.format(self.svc.name))
        else:
            warning_request(self.svc.name, 0)
            logger.warning('{} status : FAIL'.format(self.svc.name))


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


