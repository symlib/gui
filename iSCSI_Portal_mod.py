# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
# from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"


class ISCSIPortalMod(unittest.TestCase):
    def test_iscsi_portal_mod(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(2)
        driver.find_element_by_link_text("Portal").click()
        time.sleep(2)
        if "No iSCSI Portal detected." in driver.find_element_by_xpath("//table/tbody").text:
            ValError.append("pass")
            tolog("No iSCSI Portal detected")
        else:
            if driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/input").is_enabled():
                driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/input").click()
                time.sleep(0.5)
                driver.find_element_by_xpath("//button[@title='Modify iSCSI Portal Settings']").click()
                time.sleep(2)
                TCP_Port_number = random.randint(0, 65535)
                driver.find_element_by_name("tcpportnumber").clear()
                time.sleep(0.5)
                driver.find_element_by_name("tcpportnumber").send_keys(TCP_Port_number)
                time.sleep(0.5)
                IP_Type = random.choice(["IPv4", "IPv6"])
                Select(driver.find_element_by_name("ip_type")).select_by_visible_text(IP_Type)
                time.sleep(1)
                if not driver.find_element_by_xpath("//form/div[7]/div[1]/label/input").is_selected():
                    driver.find_element_by_xpath("//form/div[7]/div[1]/label/input").click()
                    time.sleep(0.5)
                driver.find_element_by_xpath("//button[@type='submit']").click()
                time.sleep(1)
                for k in range(20):
                    if "iSCSI portal settings were changed successfully." in driver.find_element_by_xpath(
                            "//body/div/div/div[5]/div/div").text:
                        ValError.append("pass")
                        tolog("iSCSI portal settings were changed successfully.")
                        break
                    if "Failed to change iSCSI portal settings" in driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text:
                        ValError.append("fail")
                        tolog(driver.find_element_by_xpath("//body/div/div/div[5]/div/div/span").text)
                        break
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
