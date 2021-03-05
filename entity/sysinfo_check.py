# coding: utf-8
# !/bin/python

import subprocess
from multiprocessing import cpu_count
import traceback
from logger.logger import logger
from config.config_init import config
import os.path


class Disk(object):
    def __init__(self):
        self.size = 0
        self.used = 0
        self.avail = 0
        self.percent = 0

        self.get_disk()

    def __str__(self):
        return 'disk status: ' + '\nsize: ' + str(self.size) + '\nused: ' + str(self.used) + '\navail: ' + str(self.avail) + '\npercent: ' + str(self.percent) + ' %'

    # initialize data
    def get_disk(self):
        try:
            # todo main dir
            main_dir = config.disk_info()['main_dir']
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
        return "\nupload is : " + str(self.upload) + "\ncpu usage: " + str(self.percent) + " %"

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

    # ReturnType float
    def get_cpu_percent(self):
        try:
            result = subprocess.Popen("ps -aux --sort -pcpu | awk '{sum+=$3} END {print sum}'", shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.percent = float(result.stdout.readline().strip('\n'))
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

        self.get_mem_info()

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
        except Exception as e:
            logger.error(traceback.format_exc())



