# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class ISCSILoggedInDevice(unittest.TestCase):
    def test_iscsi_logged_in_device_view(self):
        ValError = []
        Failflag = False
        portal_dict = {}
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(1)
        driver.find_element_by_xpath("//ul/li[9]/ul/li[8]/a").click()
        time.sleep(2)
        if "No iSCSI Initiator detected." in driver.find_element_by_xpath("//table/tbody").text:
            tolog("No logged in device was detected")
            ValError.append("pass")
        else:
            temp = driver.find_element_by_xpath("//table/tbody").text.split("\n")
            for i in temp:
                if i != "":
                    tolog(i)
                    ValError.append("pass")
                else:
                    ValError.append("fail")
        for err in ValError:
            if err == "fail":
                Failflag = True
                break
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
