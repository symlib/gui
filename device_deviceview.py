# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from login_ds import loginFirefox
from to_log import tolog
import unittest, time, re
Pass = "'result': 'p'"
Fail = "'result': 'f'"

class DeviceDeviceview(unittest.TestCase):
    def test_device_deviceview(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("Device View").click()
        time.sleep(1)
        driver.find_element_by_link_text("Front View").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//pr-page-header/div/div/div[1]/h3").text == "Front View":
            ValError.append("pass")
            tolog("Device page, Front view title was listed")
        else:
            ValError.append("fail")
            tolog("Device page, Front view title was not listed")
        driver.find_element_by_link_text("Back View").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//pr-page-header/div/div/div[1]/h3").text == "Back View":
            ValError.append("pass")
            tolog("Device page, Back view title was listed")
        else:
            ValError.append("fail")
            tolog("Device page, Back view title was not listed")
        driver.find_element_by_xpath("//pr-switch-buttons/div/a[2]/i").click()
        time.sleep(5)
        driver.find_element_by_link_text("Topology View").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//pr-page-header/div/div/div[1]/h3").text == "Topology View":
            ValError.append("pass")
            tolog("Device page, Topology view title was listed")
        else:
            ValError.append("fail")
            tolog("Device page, Topology view title was not listed")
        for val in ValError:
            if val == "fail":
                Failflag = True
        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
