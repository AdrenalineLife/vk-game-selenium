# coding: utf-8

import time
import sys
import re
import os

from selenium import webdriver
from selenium.webdriver.opera.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class DriverBase(object):
    def __init__(self, config, profile):
        self.config = config

        self.options = Options()
        #self.options.add_argument("lang=en-US")
        self.options.add_argument("mute-audio")

        version = self.choose_version(self.config['opera_path'])
        self.options.binary_location = os.path.join(self.config['opera_path'], version, 'opera.exe')
        self.options.add_argument('user-data-dir=' + profile)

        self.d = None  # instance of the webdriver

    def _elem_to_str(self, e):
        return e.get_attribute('outerHTML')

    def _print_all_elems(self, e):
        for x in e.find_elements_by_css_selector("*"):
            print(self._elem_to_str(x))

    # choose the latest browser version in the folder
    def choose_version(self, folder):
        return sorted([f.name for f in os.scandir(folder) if f.is_dir() and re.match(r'[\d.]+', f.name)])[-1]

    def open_browser(self):
        self.d = webdriver.Opera(options=self.options)
        #self.d.maximize_window()