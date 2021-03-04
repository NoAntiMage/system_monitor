# coding: utf-8
# !/bin/python

import subprocess
from multiprocessing import cpu_count
import traceback
from logger.logger import *


class Disk(object):
    def __init__(self):
        self.size = 0
        self.used = 0
        self.avail = 0
        self.percent = 0

        self.get_disk()

    def __str__(self):
        return 'disk status: ' + '\nsize: ' + str(self.size) + '\nused: ' + str(self.used) + '\navail:' + str(self.avail) + '\npercent:' + str(self.percent)

    # initialize data
    def get_disk(self):
        try:
            result = subprocess.Popen('df / |tail -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        self.cpu_count = cpu_count()
        self.upload = {"1m": 0.0, "5m": 0.0, "15m": 0.0}
        self.percent = float()

        self.get_upload()
        self.get_cpu_percent()

    def __str__(self):
        return "\nupload is : " + str(self.upload) + "\ncpu usage: " + str(self.percent) + " %"

    # ReturnType dict
    def get_upload(self):
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


if __name__ == '__main__':
    d = Disk()
    print(d)
    # print(type(d))
    p = Processor()
    print(p)
