# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
#from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class FCNode(unittest.TestCase):
    def test_fc_node(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        tolog("Start to List FC mgmt ---> Node info")
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("FC Management").click()
        time.sleep(2)
        driver.find_element_by_link_text("Node").click()
        time.sleep(1)
        if "Node"in driver.find_element_by_xpath("//pr-page-header/div/div/div[1]/h3").text:
            tolog("Node page, title 'Node' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, title 'Node'was not listed")
            ValError.append("fail")
        if "FC Node Information" in driver.find_element_by_xpath("//h4").text:
            tolog("Node page, title 'FC Node Information' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, title 'FC Node Information' was not listed")
            ValError.append("fail")
        if "WWNN:" in driver.find_element_by_xpath("//dl[1]/dt").text:
            tolog("Node page, 'WWNN:' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, 'WWNN:' was not listed")
            ValError.append("fail")
        if "Supported FC Class:" in driver.find_element_by_xpath("//dl[2]/dt").text:
            tolog("Node page, 'Supported FC Class:' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, ' Supported FC Class:' was not listed")
            ValError.append("fail")
        if "Max Frame Size:" in driver.find_element_by_xpath("//dl[3]/dt").text:
            tolog("Node page, 'Max Frame Size:' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, ' Supported FC Class:' was not listed")
            ValError.append("fail")
        if "Supported Speed:" in driver.find_element_by_xpath("//dl[4]/dt").text:
            tolog("Node page, 'Supported Speed:' was listed")
            ValError.append("pass")
        else:
            tolog("Node page, 'Supported Speed:' was not listed")
            ValError.append("fail")
        for val in ValError:
            if val == "fail":
                Failflag = True
        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
