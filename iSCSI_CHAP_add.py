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

class ISCSIChapAdd(unittest.TestCase):
    def test_iscsi_chap_add(self):
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
        driver.find_element_by_xpath("//li[9]/ul/li[7]/a").click()
        time.sleep(2)
        tolog("Start to add iSCSI CHAP entry")
        if "No iSCSI CHAP detected." in driver.find_element_by_xpath("//table/tbody").text:
            chap_count = 0
        else:
            chap_count = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        driver.find_element_by_xpath("//button[@title='Add iSCSI CHAP Information']").click()
        time.sleep(2)
        chap_name = ""
        tep = "0123456789abcdefghijklmnopqrstuvwxyz_"
        name_len = random.randint(1,31)
        for i in range(name_len):
            chap_name += random.choice(tep)
        driver.find_element_by_name("chapName").clear()
        driver.find_element_by_name("chapName").send_keys(chap_name)
        if "Local" in driver.find_element_by_xpath("//table/tbody").text.split("\n"):
            chap_type = "Peer"
        else:
            chap_type = random.choice(["Local", "Peer"])
        Select(driver.find_element_by_xpath("//form/div[2]/div/select")).select_by_visible_text(chap_type)
        time.sleep(1)
        driver.find_element_by_xpath("//form/div[3]/div[1]/input").clear()
        chap_secret = ""
        chap_secret_len = random.randint(12,16)
        for n in range(chap_secret_len):
            chap_secret += chr(random.randint(32,126))
        #print "chap_secret ------",chap_secret,chap_secret_len
        driver.find_element_by_xpath("//form/div[3]/div[1]/input").send_keys(chap_secret)
        driver.find_element_by_xpath("//form/div[4]/div[1]/input").clear()
        driver.find_element_by_xpath("//form/div[4]/div[1]/input").send_keys(chap_secret)
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        chap_count_new = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        if chap_count_new > chap_count:
            ValError.append("pass")
            tolog("Add iSCSI CHAP entry, PASS")
        else:
            ValError.append("fail")
            tolog("Add iSCSI CHAP entry, FAIL")
        for val in ValError:
            if val == "fail":
                Failflag = True
        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)
        chap_entrys = driver.find_element_by_xpath("//table/tbody").text.split("\n")
        #print "chap_entrys----",chap_entrys
        chap_index = str(chap_entrys[-1]).split()[0]
        return chap_index,chap_name,chap_secret




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


