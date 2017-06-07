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

class ISCSILoggedInDeviceAddtoinitiator(unittest.TestCase):
    def test_iscsi_loggedindevice_addtoinitiator(self):
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
            device_count = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
            tolog("Start to add device to initiator!")
            for k in range(device_count):
                if driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/input" % str(k +2)).is_enabled():
                    driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/input" % str(k + 2)).click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//button[@title='Add to Initiator List']").click()
                    time.sleep(5)
                    tolog("Check whether Device was added to initiator")
                    if driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/input" % str(k + 2)).is_enabled() == False:
                        ValError.append("pass")
                        tolog("Add device to initiator, PASS")
                    else:
                        ValError.append("fail")
                        tolog("Add device to initiator, FAIL")
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
