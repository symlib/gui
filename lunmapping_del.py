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
from to_log import tolog
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class LunmappingDel(unittest.TestCase):
    def test_lunmapping_del(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        tolog("Start to DELETE ALL LUN Mapping entries.")
        driver.find_element_by_link_text("Volume").click()
        time.sleep(2)
        driver.find_element_by_link_text("LUN Mapping & Masking").click()
        time.sleep(4)
        if "No LUN mapping entry available." in driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"):
            tolog("No lun mapping entry to be deleted")
            ValError.append("pass")
        else:
            lunmapping_count = len(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"))
            while lunmapping_count > 0:
                driver.find_element_by_xpath("//b").click()
                time.sleep(1)
                driver.find_element_by_link_text("Delete").click()
                time.sleep(1)
                driver.find_element_by_name("name").clear()
                time.sleep(1)
                driver.find_element_by_name("name").send_keys("confirm")
                time.sleep(1)
                driver.find_element_by_xpath("//button[@type='submit']").click()
                lunmapping_count -= 1
                time.sleep(3)
            if "No LUN mapping entry available." in driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"):
                tolog("All LUN Mapping entrys were deleted!")
                ValError.append("pass")
            else:
                Failflag = True
                tolog("Failed to delete All lunmapping entry!")
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