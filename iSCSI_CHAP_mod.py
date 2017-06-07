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
from iSCSI_CHAP_add import ISCSIChapAdd
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class ISCSIChapMod(unittest.TestCase):
    def test_iscsi_chap_mod(self):
        ValError = []
        Failflag = False
        tolog("First,Add a new CHAP,then Modify it")
        chap_index,chap_name, chap_secret = ISCSIChapAdd.test_iscsi_chap_add(self)
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
        tolog("Start to Modify iSCSI CHAP entry")
        driver.find_element_by_xpath("//table/tbody/tr[%d]/td[1]/input" % int(chap_index) + 2).click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@title='Modify iSCSI CHAP Settings']").click()
        time.sleep(1)
        new_chap_name = chap_name.upper()
        driver.find_element_by_xpath("//form/div[1]/div/input").clear()
        time.sleep(0.5)
        driver.find_element_by_xpath("//form/div[1]/div/input").send_keys(new_chap_name)
        time.sleep(0.5)
        driver.find_element_by_xpath("//form/div[4]/div[1]/input").clear()
        driver.find_element_by_xpath("//form/div[4]/div[1]/input").send_keys(chap_secret)
        time.sleep(1)
        new_pwd = chap_secret.upper()
        driver.find_element_by_xpath("//form/div[5]/div[1]/input").clear()
        driver.find_element_by_xpath("//form/div[5]/div[1]/input").send_keys(new_pwd)
        time.sleep(1)
        driver.find_element_by_xpath("//form/div[6]/div[1]/input").clear()
        driver.find_element_by_xpath("//form/div[6]/div[1]/input").send_keys(new_pwd)
        time.sleep(0.5)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(4)
        tolog("Completed modify CHAP, start to verify it.")
        for line in (driver.find_element_by_xpath("//table/tbody").text.split("\n")):
            if new_chap_name in line:
                ValError.append("pass")
                tolog("Modify CHAP, PASS")
            else:
                ValError.append("fail")
                tolog("Modify CHAP, FAIL")
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
