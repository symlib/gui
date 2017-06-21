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
from time import sleep
from to_log import tolog
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class IscsiTargetMod(unittest.TestCase):
    def test_iscsi_target_mod(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        sleep(3)
        driver.find_element_by_link_text("iSCSI Management").click()
        sleep(1)
        driver.find_element_by_link_text("Target").click()
        sleep(2)
        driver.find_element_by_xpath("//button[@type='button']").click()
        sleep(2)
        driver.find_element_by_name("nodealias").clear()
        #produce random length target alias
        tempp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        target_alias = ""
        def pro_name():
            n = random.randint(0,32)
            return n
        count_name = pro_name()
        for x in range(0,count_name):
            target_alias += random.choice(tempp)

        sleep(1)
        driver.find_element_by_name("nodealias").send_keys(target_alias)
        sleep(1)
        if driver.find_element_by_name("keepalive").is_selected():
            driver.find_element_by_name("keepalive").send_keys(Keys.SPACE)
            keepalive = "Disable"
        else:
            driver.find_element_by_name("keepalive").click()
            keepalive = "Enable"
        sleep(1)
        if driver.find_element_by_name("headerdigest").is_selected():
            driver.find_element_by_name("headerdigest").send_keys(Keys.SPACE)
            headerdigest = "Disable"
        else:
            driver.find_element_by_name("headerdigest").click()
            headerdigest = "Enable"
        sleep(1)
        if driver.find_element_by_name("datadigest").is_selected():
            driver.find_element_by_name("datadigest").send_keys(Keys.SPACE)
            datadigest = "Disable"
        else:
            driver.find_element_by_name("datadigest").click()
            datadigest = "Enable"
        sleep(1)
        '''
        if driver.find_element_by_name("unichapauth").is_selected():
            driver.find_element_by_name("unichapauth").send_keys(Keys.SPACE)
            unichapauth = "Disable"
        else:
            driver.find_element_by_name("unichapauth").click()
            unichapauth = "Enable"
        sleep(1)
        '''
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(4)
        driver.find_element_by_xpath("//a/small[1]").click()
        time.sleep(3)
        target_info = str(driver.find_element_by_xpath("//div[3]/div[2]/div/div/div[2]/div/div/div").text).split("\n")
        target_dict = {}
        for i in range(len(target_info)):
            if i % 2 == 0:
                target_dict[target_info[i]] =target_info[i+1]
        print "target dict is:", target_dict

        if target_dict.get("Alias:") == target_alias:
            tolog('iscsi target alias setting, PASS')
            ValError.append("pass")
        else:
            ValError.append("fail")
            tolog('iscsi target alias setting, FAIL')
        if target_dict.get("Keep Alive:") == keepalive:
            tolog('iscsi target "Keep Alive" setting, PASS')
            ValError.append("pass")
        else:
            ValError.append("fail")
            tolog('iscsi target "Keep Alive" setting, FAIL')
        if target_dict.get("Header Digest:") == headerdigest:
            tolog('iscsi target "Header Digest" setting, PASS')
            ValError.append("pass")
        else:
            ValError.append("fail")
            tolog('iscsi target "Header Digest" setting, FAIL')
        if target_dict.get("Data Digest:") == datadigest:
            tolog('iscsi target "Data Digest" setting, PASS')
            ValError.append("pass")
        else:
            ValError.append("fail")
            tolog('iscsi target "Data Digest" setting, FAIL')
        '''
        if target_dict.get("Uni-directional CHAP Authentication:") == unichapauth:
            tolog('iscsi target "Uni - directional CHAP Authentication" setting, PASS')
            tolog("pass")
        else:
            ValError.append("fail")
            tolog('iscsi target "Uni - directional CHAP Authentication" setting, FAIL')
        '''
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
