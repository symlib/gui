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

class FCLoggedindevice(unittest.TestCase):
    def test_fc_loggedindevice_addtoinitiator(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("FC Management").click()
        time.sleep(1)
        driver.find_element_by_link_text("Logged In Device").click()
        time.sleep(2)
        port_entrys = driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")
        i = 2
        while i > 0:
            tolog("Start FC mgmt ---> Logged in Device, test 'Add to Initiator List")
            line_select = random.randint(2, len(port_entrys) + 1)
            driver.find_element_by_xpath("//table[2]/tbody/tr[%d]/td[1]/input" % line_select).click()
            time.sleep(1)
            if not driver.find_element_by_xpath("//pr-button-bar/div/div/div/button[2]").is_enabled():
                tolog("This device entry had been add into initiator list, change another one")
                ValError.append("pass")
            else:
                driver.find_element_by_xpath("//pr-button-bar/div/div/div/button[2]").click()
                time.sleep(1)
                if "successfully" in driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text:
                    tolog(driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text)
                    ValError.append("pass")
                elif "already" in driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text:
                    tolog(driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text)
                    ValError.append("pass")
                else:
                    tolog(driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text)
                    ValError.append("fail")
                time.sleep(4)
                driver.find_element_by_xpath("//table[2]/tbody/tr[%d]/td[1]/input" % line_select).click()
                time.sleep(2)
                if not driver.find_element_by_xpath("//pr-button-bar/div/div/div/button[2]").is_enabled():
                    tolog("Verified, it was added into initiator list")
                    ValError.append("pass")
                else:
                    tolog("Verified, 'add into initiator list'button still is highlight,FAILED")
                    ValError.append("fail")
            time.sleep(1)
            i -= 1
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
