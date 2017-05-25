# -*- coding: utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest,re,random,time
from print_result import printSF
from login_ds import login
from VerifyWords import VerifyWords
from to_log import tolog
Pass="'result': 'p'"
Fail="'result': 'f'"

class ISCSIPortalView(unittest.TestCase):
    def test_iscsi_portal_view(self):
        ValError = []
        portal_dict = {}
        self.driver = login()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(1)
        driver.find_element_by_link_text("Portal").click()
        time.sleep(2)
        if "No iSCSI Portal detected." in driver.find_element_by_xpath("//table/tbody").text:
            tolog("No iSCSI Portal entry was detected")
            tolog(Pass)
        else:
            temp = driver.find_element_by_xpath("//table/tbody").text.split("\n")
            for p in temp:
                portal_dict[str(p).split()[0]] = str(p).split()[2:6]
            if portal_dict:
                tolog("Portal list is: "+ str(portal_dict))
                tolog(Pass)
            else:
                tolog(Fail)
        return portal_dict

    
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
