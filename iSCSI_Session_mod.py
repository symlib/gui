# -*- coding: utf-8 -*-
# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random
from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class ISCSISessionMod(unittest.TestCase):
    def test_iscsi_session_mod(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(3)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(2)
        driver.find_element_by_link_text("Session").click()
        time.sleep(2)
        tolog("Start iSCSI Session Modify....!!")
        if "No session" in driver.find_element_by_xpath("//table/tbody").text:
            tolog("No session was detected")
            ValError.append("pass")
        else:
            driver.find_element_by_xpath("//tbody/tr[2]/td[1]/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//button[@title='Modify iSCSI Session Settings']").click()
            time.sleep(1)
            if driver.find_element_by_name("keepalive").is_selected():
                driver.find_element_by_name("keepalive").click()
                keepalive = "Disable"
            else:
                driver.find_element_by_name("keepalive").click()
                keepalive = "Enable"
            driver.find_element_by_xpath("//button[@type='submit']").click()

            tolog("Starting verify iSCSI Port settings!")
            for k in range(20):
                driver.find_element_by_xpath("//tbody/tr[2]/td[1]/input").click()
                time.sleep(1)
                driver.find_element_by_xpath("//button[@title='View iSCSI Session Information']").click()
                time.sleep(1)
                if driver.find_element_by_xpath("//dl[14]/dd[1]").text == "Enable":
                    tolog("Modify Session, PASS")
                    ValError.append("pass")
                    break
                else:
                    tolog("Modify Session, FAIL")
                    tolog("KeepAlive is %s, now" % driver.find_element_by_xpath("//dl[14]/dd[1]").text)
                    ValError.append("fail")
                    break
        for err in ValError:
            if err == "fail":
                Failflag = True
        tolog("iSCSI Port Modify, completed")
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
