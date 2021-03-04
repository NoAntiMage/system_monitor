# coding: utf-8
# Description: 适用于单点服务检测
import socket
import httplib
import subprocess
import traceback
import re
from logger.logger import logger
from config.config_init import config


# Description: private object
class AppCheck(object):
    def __init__(self, name, address='127.0.0.1'):
        self.name = name
        self.address = address
        self.pid = 1
        self.port = 0
        self.port_check_cmd = "ss -tunlp | grep {}".format(self.name)
        self.process_status = False
        self.listen_status = False
        self.connect_status = False
        self.request_status = False

        logger.info('Checking {} status'.format(self.name))

    # Description: 组合检测监控指标 [进程运行，端口监听，端口连接，接口请求]
    def auto_check(self):
        self.process_status = self.process_check()
        if self.process_status is True:
            self.listen_status = self.port_listen_check()
            if self.listen_status is True:
                self.connect_status = self.port_request_check()
                if self.connect_status is True:
                    self.request_status = self.api_check()

    # ReturnType boolean
    def process_check(self):
        try:
            cmd = 'ps -ef | grep {} | grep -v grep '.format(self.name)
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            line = result.stdout.readline()
            if len(line) > 0:
                self.pid = line.split()[1]
                logger.info('{} is running with pid {}'.format(self.name, self.pid))
                return True
            else:
                logger.error('{} is not running'.format(self.name))
                return False
        except Exception as e:
            logger.error(traceback.format_exc())

    # ReturnType boolean
    def port_listen_check(self):
        try:
            result = subprocess.Popen(self.port_check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            line = result.stdout.readline()
            if line and 'LISTEN' in line:
                self.port = int(line.split()[4].split(':')[-1])
                logger.info('{} is listening at {}'.format(self.name, self.port))
                return True
            else:
                logger.warning('{} port state is not listen'.format(self.name))
                return False
        except Exception as e:
            logger.error(traceback.format_exc())

    # ReturnType boolean
    def port_request_check(self):
        try:
            s = socket.socket()
            # logger.info('Attempting to connect to %s on port %s' % (self.name, self.port))
            try:
                s.connect((self.address, self.port))
                logger.info("Connected to %s on port %s" % (self.name, self.port))
                return True
            except socket.error as e:
                logger.error("Connected to %s on port %s failed: %s" % (self.name, self.port, e))
                return False
        except Exception as e:
            logger.error(traceback.format_exc())

    def api_check(self):
        print('please override app api')


class Nginx(AppCheck):
    def __init__(self, name='nginx'):
        super(Nginx, self).__init__(name)
        self.auto_check()

    # ReturnType boolean
    def api_check(self):
        try:
            logger.info('sending request to {}'.format(self.name))
            resource = '/'
            if not resource.startswith('/'):
                resource = '/' + resource
            conn = httplib.HTTPConnection(self.address, self.port)
            try:
                logger.info('HTTP connection created successfully')
                conn.request('GET', resource)
                logger.info('sending request for %s successful' % resource)

                response = conn.getresponse()

                logger.info('response status: %s' % response.status)
            except socket.error as e:
                logger.error('HTTP connection failed: %s' % e)
                return False
            finally:
                conn.close()
                logger.info('HTTP connection closed succeesfully')
            if response.status in [200, 301]:
                logger.info('get response from {} successfully'.format(self.name))
                return True
            else:
                return False
        except Exception as e:
            logger.error(traceback.format_exc())


class Mysql(AppCheck):
    def __init__(self, name='mysql'):
        super(Mysql, self).__init__(name)
        self.auto_check()

    def api_check(self):
        try:
            logger.info('sending request to {}'.format(self.name))
            mysql_login = config.mysql_auth()
            cmd = "`which mysql` -u{} -p{} -e 'select version()'".format(mysql_login['user'], mysql_login['password'])
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            f = result.stdout.read()
            if 'version' in f:
                logger.info('get response from {} successfully'.format(self.name))
                return True
            else:
                return False
        except Exception as e:
            logger.error(traceback.format_exc())


class Redis(AppCheck):
    def __init__(self, name='redis'):
        super(Redis, self).__init__(name)
        self.auto_check()

    def api_check(self):
        try:
            logger.info('sending request to {}'.format(self.name))
            redis_login = config.redis_auth()
            cmd = "`which redis-cli` -a {} info".format(redis_login['password'])
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            f = result.stdout.read()
            if 'Server' in f:
                logger.info('get response from {} successfully'.format(self.name))
                return True
            else:
                return False
        except Exception as e:
            logger.error(traceback.format_exc())


# Description: zk 基于java服务。socket连接无法采用服务名查询，故采用端口查询
class Zookeeper(AppCheck):
    def __init__(self, name='zookeeper'):
        super(Zookeeper, self).__init__(name)
        self.get_port()
        self.port_check_cmd = "ss -tunlp | grep {}".format(self.port)
        self.auto_check()

    def api_check(self):
        try:
            logger.info('sending request to {}'.format(self.name))
            cmd = '`which zkServer.sh` status'
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            f = result.stdout.read()
            if 'Mode' in f:
                logger.info('get response from {} successfully'.format(self.name))
                return True
            else:
                return False
        except Exception as e:
            logger.error(traceback.format_exc())

    def get_port(self):
        try:
            cmd = "`which zkServer.sh` status | grep port"
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = result.stdout.readlines()
            pattern = r"port"
            for line in lines:
                result = re.search(pattern, line)
                if result:
                    self.port = int(line.split('.')[0].split(':')[-1])
                    break
            if result is None:
                raise Exception('port not found in zkServer.sh status')
            return self.port
        except Exception as e:
            logger.error(traceback.format_exc())



