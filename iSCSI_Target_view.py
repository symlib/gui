# -*- coding: utf-8 -*-
# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest,re,random
from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from time import sleep
from to_log import tolog
Pass = "'result': 'p'"
Fail = "'result': 'f'"

class IscsiTargetView1(unittest.TestCase):
    def test_iscsi_target_view(self):
        Failflag = False
        ValError = []
        errlist=[]
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        sleep(2)
        driver.find_element_by_xpath("//li[9]/a/span/span").click()
        sleep(2)
        driver.find_element_by_xpath("//li[9]/ul/li/a/span/span").click()
        sleep(3)
        try:
            self.assertEqual("Target", driver.find_element_by_css_selector("h3.ng-binding").text)
            tolog("Title 'Target' was displayed.")
            ValError.append("pass")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            tolog("Title 'Target' was not displayed!!!")
            ValError.append("fail")
        sleep(1)
        try:
            self.assertEqual("iSCSI Target Information", driver.find_element_by_css_selector("h4.header-title.ng-binding").text)
            tolog("Title 'iSCSI Target Information' was displayed.")
            ValError.append("pass")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            ValError.append("fail")
        sleep(1)
        try:
            self.assertEqual("ID:", driver.find_element_by_css_selector("dt.col-sm-3.ng-binding").text)
            tolog("iSCSI Target Information page,'ID' was displayed.")
            ValError.append("pass")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            ValError.append("fail")
        sleep(1)
        try:
            self.assertEqual("Status:", driver.find_element_by_xpath("//dl[2]/dt").text)
            tolog("iSCSI Target Information page,'Status' was displayed.")
            ValError.append("pass")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            ValError.append("fail")
        sleep(1)
        try:
            self.assertEqual("Name:", driver.find_element_by_xpath("//dl[3]/dt").text)
            tolog("iSCSI Target Information page,'Name' was displayed.")
            ValError.append("pass")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            ValError.append("fail")
        for val in ValError:
            if val == "fail":
                Failflag = True
        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)


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

