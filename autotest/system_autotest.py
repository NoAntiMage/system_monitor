import unittest
import os
import subprocess
from template.warning_msg import *

project_path = os.path.dirname(os.path.dirname(__file__))
main_file = os.path.join(project_path, 'main.py')


# TODO
class DiskTestCase(unittest.TestCase):
    pass


class InputOutputTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(InputOutputTestCase, self).__init__(methodName)
        self.cmd = '`which python` {}'.format(main_file)
        self.stout_fd = 0

    def setUp(self):
        os.system("nohup stress-ng -i 10 --hdd 1 --timeout 60 &")
        self.stdout_fd = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()

    def test_await(self):
        self.assertIn(io_delay_warning, self.stdout_fd)

    # TODO
    def test_io_queue(self):
        self.assertEqual(0, 0)

    def tearDown(self):
        os.system("ps -ef | grep stress | awk '{print $2}' | xargs kill -9 > /dev/null 1>&2")


if __name__ == '__main__':
    unittest.main()
