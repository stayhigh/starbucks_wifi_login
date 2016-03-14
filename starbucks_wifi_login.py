# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re
import sys
from getpass import getpass

def show_usage():
    print "python %s <starbucks_account>" % sys.argv[0]

"""
if len(sys.argv) != 2:
    show_usage()
    exit(1)
"""
MOBILE_TYPE, NOTEBOOK_TYPE, TABLET_TYPE = (1, 2, 3)
DEFAULT_TYPE = NOTEBOOK_TYPE

starbucks_account = "YOUR_STARBUCKS_ACCOUNT"
starbucks_passwd =  getpass("Input your password for starbucks wifi:")

class UseStarbuckWifi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.wifly.com.tw/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_starbucks_wifi_login(self):
        driver = self.driver
        driver.get(self.base_url + "/StarbucksFree/rule.aspx?DeviceKind=2&RTYPE=" + str(DEFAULT_TYPE))
        driver.find_element_by_css_selector("a > img").click()
        driver.find_element_by_id("textfield5").clear()
        driver.find_element_by_id("textfield5").send_keys(starbucks_account)
        driver.find_element_by_id("textfield").clear()
        driver.find_element_by_id("textfield").send_keys(starbucks_passwd)
        driver.find_element_by_id("RadioGroup1_1").click()
        driver.find_element_by_css_selector("img[alt=\"12\"]").click()
        driver.implicitly_wait(30)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
