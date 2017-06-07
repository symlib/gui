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

class ISCSIPortMod(unittest.TestCase):
    def test_iscsi_port_mod(self):
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
        driver.find_element_by_xpath("//li[9]/ul/li[2]/a").click()
        time.sleep(2)
        tolog("Start iSCSI Port settings!!")
        driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/input").click()
        #driver.find_element_by_xpath("//table/tbody/tr[5]/td[1]/input").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@title='Modify iSCSI Port Settings']").click()
        time.sleep(1)
        if driver.find_element_by_xpath("//form/div[3]/div/label/input").is_selected():
            driver.find_element_by_xpath("//form/div[3]/div/label/input").click()
            time.sleep(1)
            Port_status = "Disable"
        else:
            driver.find_element_by_xpath("//form/div[3]/div/label/input").click()
            time.sleep(1)
            Port_status = "Enable"

        if driver.find_element_by_xpath("//form/div[4]/div[1]/label/input").is_selected():
            driver.find_element_by_xpath("//form/div[4]/div/label/input").click()
            JumboF_status = "Disable"
            time.sleep(1)
        else:
            driver.find_element_by_xpath("//form/div[4]/div/label/input").click()
            JumboF_status = "Enable"
            time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        tolog("Starting verify iSCSI Port settings!")
        for k in range(20):
            if "iSCSI port settings were changed successfully." in driver.find_element_by_xpath(
                    "//body/div/div/div[5]/div").text:
                driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/input").click()
                #driver.find_element_by_xpath("//table/tbody/tr[5]/td[1]/input").click()
                time.sleep(0.5)
                driver.find_element_by_xpath("//button[@title='View iSCSI Port Information']").click()
                time.sleep(1)
                if driver.find_element_by_xpath("//dl[2]/dd[2]").text == Port_status:
                    tolog("iSCSI Port -> Port status modify, PASS")
                    ValError.append("pass")
                else:
                    tolog("iSCSI Port -> Port status modify, Fail")
                    ValError.append("fail")
                if driver.find_element_by_xpath("//dl[2]/dd[1]").text == JumboF_status:
                    tolog("iSCSI Port -> Jumbo Frame status modify, PASS")
                    ValError.append("pass")
                else:
                    tolog("iSCSI Port -> Jumbo Frame status modify, Fail")
                    ValError.append("fail")
                break
            if "Operation failed as the specified port belongs to a trunk" in driver.find_element_by_xpath(
                        "//body/div/div/div[5]/div").text:
                ValError.append(Pass)
                tolog("Failed to change iSCSI port settings.Operation failed as the specified port belongs to a trunk")
                break
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
