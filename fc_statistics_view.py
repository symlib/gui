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

class FCStatisticsView(unittest.TestCase):
    def test_fc_statisticsView(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        tolog("Start FC mgmt ---> Statistics View")
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("FC Management").click()
        time.sleep(1)
        driver.find_element_by_link_text("Statistics").click()
        time.sleep(2)
        port_entrys = driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")
        line_select = random.randint(2, len(port_entrys) + 1)
        driver.find_element_by_xpath("//table[2]/tbody/tr[%d]/td[1]/input" % line_select).click()
        time.sleep(1)
        driver.find_element_by_xpath("//pr-button-bar/div/div/div/button[1]").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//body/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div/div").text != "":
            tolog(driver.find_element_by_xpath("//body/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div/div").text)
            ValError.append("pass")
        else:
            tolog("Failed to View statistics")
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
