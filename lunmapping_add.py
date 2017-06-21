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

class LunmappingAdd(unittest.TestCase):
    def test_lunmapping_add(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        tolog("Start to create LUN Mapping.")
        driver.find_element_by_link_text("Volume").click()
        time.sleep(2)
        driver.find_element_by_link_text("LUN Mapping & Masking").click()
        time.sleep(4)
        if "No LUN mapping entry available." in driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"):
            lunmappint_entry_start = 0
        else:
            lunmappint_entry_start = len(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"))
        if driver.find_element_by_xpath("//pr-buttons/button[2]").is_enabled():
            driver.find_element_by_xpath("//pr-buttons/button[2]").click()
            time.sleep(3)
            driver.find_element_by_xpath("//table/thead/tr/th[1]/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//div[3]/div[1]/button[2]").click()
            time.sleep(2)
            driver.find_element_by_link_text("Snapshot").click()
            time.sleep(2)
            driver.find_element_by_xpath("//div[3]/div[1]/button[2]").click()
            time.sleep(2)
            driver.find_element_by_link_text("Clone").click()
            time.sleep(1)
            driver.find_element_by_xpath("//div[3]/div[1]/button[2]").click()
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(3)
            driver.find_element_by_xpath("//div[3]/button").click()
            time.sleep(6)
            lunmappint_entry_end = len(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"))
            if lunmappint_entry_end > lunmappint_entry_start:
                ValError.append("pass")
                tolog("Add lun mapping succeed")
            else:
                ValError.append("fail")
                tolog("Add lun mapping failed")
        else:
            tolog("LUN Mapping button is grey, No initiator entry was added.")
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
