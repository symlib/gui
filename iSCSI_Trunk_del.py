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
from login_ds import login
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"


class ISCSITrunkDel(unittest.TestCase):
    def test_iscsi_trunk_del(self):
        ValError = []
        Failflag = False
        self.driver = login()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(2)
        driver.find_element_by_link_text("Trunk").click()
        time.sleep(2)
        if "No iSCSI Trunk detected" in driver.find_element_by_xpath("//table/tbody").text:
            trunk_count = 0
        else:
            trunk_count = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        print "Trunk list count is :", trunk_count
        if "No iSCSI Trunk detected" in str(driver.find_element_by_xpath("//table/tbody").text.split("\n")):
            tolog("No iSCSI Trunk detected")
            tolog(Pass)
        else:
            while trunk_count > 0:
                driver.find_element_by_xpath("//b").click()
                time.sleep(1)
                driver.find_element_by_link_text("Delete").click()
                time.sleep(1)
                driver.find_element_by_name("name").clear()
                time.sleep(1)
                driver.find_element_by_name("name").send_keys("confirm")
                time.sleep(1)
                driver.find_element_by_xpath("//button[@type='submit']").click()
                trunk_count -= 1
                time.sleep(3)
            if "No iSCSI Trunk detected" in str(driver.find_element_by_xpath("//table/tbody").text.split("\n")):
                tolog("All iSCSI Trunk entry were deleted!")
                tolog(Pass)
            else:
                Failflag = True
                tolog("Failed to delete All iSCSI Trunk entry!")
                tolog(Fail)

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
