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

class GetPdInfo(unittest.TestCase):
    def test_get_pd_info(self):
        ValError = []
        Result = "'result': 'p'"
        self.driver = login()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        unconfig_pd = []
        config_pd = []
        dead_pd = []
        pd_list = {}
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("Physical Drive").click()
        time.sleep(8)
        if driver.find_element_by_xpath("//body/div[1]/div/div[3]/div[2]").text == "":
            ValError.append("fail")
        else:
            all_pd = str(driver.find_element_by_xpath("//table/tbody").text)
            pd_text = str(driver.find_element_by_xpath("//table/tbody").text).split("\n")
            for i in range(len(pd_text)):
                if i % 2 == 0:
                    pd_list[pd_text[i]] = pd_text[i + 1]
            for p in pd_list.items():
                if "Unconfigured" in p[1]:
                    unconfig_pd.append(p[0])
                if "Pool" in p[1]:
                    config_pd.append(p[0])
            tolog("All PD info is: ")
            tolog(all_pd)
            tolog("Unconfigured PD ID is: %s" % str(unconfig_pd))
            tolog("Configured PD ID is: %s" % str(config_pd))
        if "fail" in ValError:
            tolog("Get PD list, FAILED!!")
            Result = "'result': 'f'"
        else:
            tolog("Get PD list, PASS!!")
            Result = "'result': 'p'"

        return pd_list, unconfig_pd,config_pd,Result

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
