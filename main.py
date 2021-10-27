# coding: utf-8
# !/usr/bin/python

import sys
import os
from monitor.monitor import *
from config.config_init import config

sys.path.append(os.path.dirname(__file__))


def main():
    logger.info("   HEALTH CHECKING...")
    if config.has_section("disk") and config.get("disk", "onboot") == "yes":
        disk_check()
    if config.has_section("cpu") and config.get("cpu", "onboot") == "yes":
        cpu_check()
    if config.has_section("memory") and config.get("memory", "onboot") == "yes":
        memory_check()
    if config.has_section("input-output") and config.get("input-output", "onboot") == "yes":
        io_check()

    # nginx_check()
    # mysql_check()
    # redis_check()
    # zookeeper_check()


if __name__ == '__main__':
    main()


