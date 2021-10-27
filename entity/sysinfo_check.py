# coding: utf-8
# !/bin/python

import subprocess
from multiprocessing import cpu_count
import traceback
from logger.logger import logger
from config.config_init import config
import os.path
from util.formatutil import pretty_format


class Disk(object):
    def __init__(self):
        self.size = 0
        self.used = 0
        self.avail = 0
        self.percent = 0

        self.get_disk()

    def __str__(self):
        return '\ndisk status: \n' \
               + pretty_format('size: {} Kb\n'.format(self.size)) \
               + pretty_format('used: {} Kb\n'.format(self.used)) \
               + pretty_format('avail: {} Kb\n'.format(self.avail/1024)) \
               + pretty_format('percent: {} %\n'.format(self.percent))

    # initialize data
    def get_disk(self):
        try:
            main_dir = config.get('disk', 'main_dir')
            cmd = 'df {} |tail -1'.format(main_dir)
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            line = result.stdout.readline().strip('\n')
            free = line.split()
            self.size = int(free[1])
            self.used = int(free[2])
            self.avail = int(free[3])
            self.percent = int(free[4].strip('%'))
        except Exception as e:
            logger.error(traceback.format_exc())


class Processor(object):
    def __init__(self):
        self.loadavg_path = '/proc/loadavg'
        self.cpu_count = cpu_count()
        self.upload = {"1m": 0.0, "5m": 0.0, "15m": 0.0}
        self.percent = float()

        self.get_upload()
        self.get_cpu_percent()

    def __str__(self):
        # return "cpu status:\nupload is : " + str(self.upload) + "\ncpu usage: " + str(self.percent) + " %"
        return "\ncpu status:\n" \
                + pretty_format("upload in 1m: {}\n".format(self.upload['1m'])) \
                + pretty_format("upload in 5m: {}\n".format(self.upload['5m'])) \
                + pretty_format("upload in 15m: {}\n".format(self.upload['15m'])) \
                + pretty_format("usage percent: {} %\n".format(self.percent))

    # ReturnType: dict
    def get_upload(self):
        try:
            if not os.path.isfile(self.loadavg_path):
                raise Exception('{} does not exist.'.format(self.loadavg_path))
            with open(self.loadavg_path, 'r') as f:
                result = f.readline()
                upload = result.split()
                self.upload["1m"] = float(upload[0])
                self.upload["5m"] = float(upload[1])
                self.upload["15m"] = float(upload[2])
                assert type(self.upload) == dict
                return self.upload
        except Exception as e:
            logger.error(traceback.format_exc())

    # status: DEPRECATED
    # ReturnType dict
    def get_upload_by_uptime(self):
        try:
            result = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            upload = result.stdout.readline().strip("\n").split(":")[-1].split(",")
            assert len(upload) == 3
            self.upload["1m"] = float(upload[0])
            self.upload["5m"] = float(upload[1])
            self.upload["15m"] = float(upload[2])
            assert type(self.upload) == dict
            return self.upload
        except Exception as e:
            logger.error(traceback.format_exc())

    # Discription: 处理器空闲状态以外的时间占比
    # ReturnType float
    def get_cpu_percent(self):
        try:
            result = subprocess.Popen("mpstat | tail -1", shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            idle = float(result.stdout.readline().strip('\n').split()[-1])
            self.percent = round(100 - idle, 2)
            assert type(self.percent) == float
            return self.percent
        except Exception as e:
            logger.error(traceback.format_exc())


class Memory(object):
    def __init__(self):
        self.mem_info_path = '/proc/meminfo'
        self.total = 0
        self.free = 0
        self.avail = 0
        self.buffer = 0
        self.cached = 0
        self.percent = 0

        self.get_mem_info()

    def __str__(self):
        return '\nmemory status:\n' \
                + pretty_format('total: {} Kb\n'.format(self.total)) \
                + pretty_format('avail: {} Kb\n'.format(self.avail)) \
                + pretty_format('usage: {} %\n'.format(round(self.percent * 100 , 2)))

    def get_mem_info(self):
        if not os.path.isfile(self.mem_info_path):
            raise Exception('{} does not exist.'.format(self.mem_info_path))
        try:
            with open(self.mem_info_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'MemTotal' in line:
                        self.total = int(line.split()[1])
                    if 'MemFree' in line:
                        self.free = int(line.split()[1])
                    if 'MemAvailable' in line:
                        self.avail = int(line.split()[1])
                    if 'Buffers' in line:
                        self.buffer = int(line.split()[1])
                    if 'Cached' in line:
                        self.cached = int(line.split()[1])
            self.percent = 1 - (round(self.avail, 2) / self.total)
            assert type(self.percent) == float

        except Exception as e:
            logger.error(traceback.format_exc())


class InputOutput(object):
    def __init__(self, device='sda'):
        if 'device' in config.options("input-output"):
            self.device = config.get('input-output', 'device')
        else:
            self.device = device

        self.await = 0
        self.util = 0

        self.get_io_info()

    def __str__(self):
        return "\nio status: \n" \
                + pretty_format('await time: {} ms\n'.format(self.await)) \
                + pretty_format('io queue usage: {} %\n'.format(self.util))

    def get_io_info(self):
        try:
            iostat = list()
            cmd = 'iostat -x'
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            iostats = result.stdout.readlines()
            for line in iostats:
                if self.device in line:
                    iostat = line.split()
                    break
            if len(iostat) != 0:
                self.await = float(iostat[9])
                self.util = float(iostat[13])
            else:
                raise Exception("device {} not found.".format(self.device))
        except Exception as e:
            logger.error(traceback.format_exc())
