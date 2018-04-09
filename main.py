# coding: utf-8

import traceback as tb
import time
import sys

from driver import VKGameDriver
from config import config


profile_path = config['profiles_path'] + config['profile_prefix']
driver = VKGameDriver(config, profile_path)
try:
    driver.start()
except Exception as e:
    tb.print_exc()
    print('Press enter to quit')
    input()
    sys.exit()
