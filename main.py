# coding: utf-8
# !/usr/bin/python

from monitor.monitor import *


def main():
    disk_check()
    cpu_check()
    memory_check()
    nginx_check()
    mysql_check()
    redis_check()
    zookeeper_check()


if __name__ == '__main__':
    main()


