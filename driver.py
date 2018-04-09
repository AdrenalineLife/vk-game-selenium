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

import config
from driver_baseclass import DriverBase


def can_make_word(word: str, letters) -> bool:
    letters = list(letters)
    for x in word:
        if x in letters:
            letters.remove(x)
        else:
            return False
    return True


class VKGameDriver(DriverBase):
    def get_word_length(self) -> int:
        return len(self.d.find_elements_by_css_selector('#word_body_block > div.word_body_word'))

    # type in the word with 'delay' between each letter
    def type_word(self, word: str, delay: float=0):
        selector = 'div.letters > div > span:not([style*="display: none"])'
        for letter in word.lower():
            next(x for x in self.d.find_elements_by_css_selector(selector)
                 if x.get_attribute('innerHTML').lower() == letter).click()
            time.sleep(delay)

    # get the letters with which we should construct the word
    def get_letters(self) -> str:
        letters = ''
        selector = 'div.letters > div > span:not([style*="display: none"])'
        for span_letter in self.d.find_elements_by_css_selector(selector):
            letters += span_letter.get_attribute('innerHTML')
        return letters

    def check_for_win(self) -> bool:
        try:
            return bool(self.d.find_element_by_css_selector('div.word_body_word').get_attribute('innerHTML'))
        except NoSuchElementException:
            return True

    # generator of suitable words
    def suitable_words(self, filepath: str, length: int, letters: str):
        with open(filepath, 'rt') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if len(line) == length and can_make_word(line, letters):
                    yield line

    def close_popups(self):
        popup_close_but = self.d.find_elements_by_css_selector('div.alert_close')
        while popup_close_but:
            for el in popup_close_but:
                try:
                    ActionChains(self.d).move_to_element(el).click(el).perform()
                    time.sleep(2)
                    popup_close_but.remove(el)
                except WebDriverException:
                    pass

    def start(self):
        self.open_browser()
        self.d.get('https://vk.com/app3584203')

        iframe = self.d.find_element_by_css_selector('iframe[src*="words.smapps.org"]')
        ActionChains(self.d).move_to_element(iframe).perform()
        self.d.switch_to.frame(iframe)
        self.close_popups()

        WebDriverWait(self.d, 15, poll_frequency=0.15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#main_play'))).click()

        # TODO PIC 4 is default, 3 rebus
        el = self.d.find_element_by_css_selector('div#main_menu_4_pic > div.main_menu_start_game > div.c')
        ActionChains(self.d).move_to_element(el).click(el).perform()
        time.sleep(1.5)

        while True:
            letters = self.get_letters().lower()
            print(letters)
            word_length = self.get_word_length()
            word_found = False
            for w in self.suitable_words('noun.txt', word_length, letters):
                self.type_word(w)
                if self.check_for_win():
                    word_found = True
                    print(w)
                    break
            if not word_found:
                print('No suitable words found')
                sys.exit()

            el = WebDriverWait(self.d, 20, poll_frequency=0.2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#game_win_block > div.game_win_next > div > div.c')))
            ActionChains(self.d).move_to_element(el).click(el).perform()
            time.sleep(1.5)



if __name__ == '__main__':
    pass
