# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog


Pass = "'result': 'p'"
Fail = "'result': 'f'"

class DeleteAllPool(unittest.TestCase):
    def test_delete_all_pool(self):
        Failflag = False
        ValError = []
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Pool").click()
        tolog("Start to delete all existing Pools")
        time.sleep(2)
        if "There is no" in driver.find_element_by_xpath("//tbody").text:
            tolog("There is no Pool")
            ValError.append("pass")
        else:
            #print "====0000", driver.find_element_by_xpath("//table[2]/tbody").text
            pool_count = len(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"))/4
            while pool_count > 0:
                driver.find_element_by_xpath("//b").click()
                time.sleep(1)
                driver.find_element_by_link_text("Delete").click()
                time.sleep(1)
                driver.find_element_by_name("name").clear()
                time.sleep(1)
                driver.find_element_by_name("name").send_keys("confirm")
                time.sleep(1)
                driver.find_element_by_xpath("//button[@type='submit']").click()
                time.sleep(4)
                pool_count -= 1
            if "There is no" in str(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")):
                tolog("All Pools were deleted!")
                ValError.append("pass")
            else:
                Failflag = True
                tolog("Failed to delete All Pool!")
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
