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
from login_ds import login
from VerifyWords import VerifyWords
from to_log import tolog
import time


class ISCSIPortView(unittest.TestCase):
    def test_iscsi_port_view(self):
        Pass = "'result': 'p'"
        Fail = "'result': 'f'"
        Failflag = False
        ValError = []
        self.driver = login()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(1)
        #driver.find_element_by_link_text("Port")
        driver.find_element_by_xpath("//li[9]/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(0.5)
        if driver.find_element_by_xpath("//h4").text == "Basic Information":
            ValError.append("pass")
            tolog("Verify title Basic Information, pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify title Basic Information, Fail")
        if driver.find_element_by_xpath("//dt").text == "Port Id:":
            tolog("Verify item Port Id, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Port Id ,Fail")
        if driver.find_element_by_xpath("//dt[2]").text == "Controller ID:":
            tolog("Verify item Controller ID, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Controller ID ,Fail")
        if driver.find_element_by_xpath("//dl[2]/dt").text == "Jumbo Frame:":
            tolog("Verify item Jumbo Frame, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Jumbo Frame ,Fail")
        if driver.find_element_by_xpath("//dl[2]/dt[2]").text == "Port:":
            tolog("Verify item Port, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Port ,Fail")
        if driver.find_element_by_xpath("//dl[3]/dt").text == "Primary MAC Address:":
            tolog("Verify item Primary MAC Address, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Primary MAC Address ,Fail")
        if driver.find_element_by_xpath("//dl[3]/dt[2]").text == "Max Support Speed:":
            tolog("Verify item Max Support Speed, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Max Support Speed ,Fail")
        if driver.find_element_by_xpath("//dl[4]/dt").text == "Current Speed:":
            tolog("Verify item Current Speed, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Current Speed ,Fail")
        if driver.find_element_by_xpath("//dl[4]/dt[2]").text == "Assigned Portals:":
            tolog("Verify item Assigned Portals, pass")
            ValError.append("pass")
        else:
            Failflag = True
            ValError.append("fail")
            tolog("Verify item Assigned Portals ,Fail")
        if "fail" in ValError:
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
