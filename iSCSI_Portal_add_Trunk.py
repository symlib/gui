# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
#from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"

class ISCSIPortalAddVlan(unittest.TestCase):
    def test_iscsi_portal_add_trunk(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("iSCSI Management").click()
        time.sleep(2)
        driver.find_element_by_link_text("Trunk").click()
        time.sleep(2)
        trunk_id = []
        for t in driver.find_element_by_xpath("//table/tbody").text.split("\n"):
            trunk_id.append(str(t.split()[0]))
        time.sleep(2)
        driver.find_element_by_link_text("Portal").click()
        time.sleep(2)
        tolog("Start to Add Portal, specify Trunk type")
        if "No iSCSI Portal detected." in driver.find_element_by_xpath("//table/tbody").text:
            portal_entry1 = 0
        else:
            portal_entry1 = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//form/div[1]/div/label[2]/input").is_enabled():
            driver.find_element_by_xpath("//form/div[1]/div/label[2]/input").click()
            time.sleep(1)
            Select(driver.find_element_by_name("trunkid")).select_by_visible_text(random.choice(trunk_id))
            time.sleep(0.5)
            TCP_Port_number = random.randint(0, 65535)
            driver.find_element_by_name("tcpportnumber").clear()
            time.sleep(0.5)
            driver.find_element_by_name("tcpportnumber").send_keys(TCP_Port_number)
            IP_Type = random.choice(["IPv4", "IPv6"])
            Select(driver.find_element_by_name("ip_type")).select_by_visible_text(IP_Type)
            time.sleep(0.5)
            if not driver.find_element_by_xpath("//form/div[5]/div[1]/label").is_selected():
                driver.find_element_by_xpath("//form/div[5]/div[1]/label").click()
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(6)
            portal_entry2 = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
            if portal_entry2 > portal_entry1:
                tolog("Add iSCSI Portal,Associated Port Type:Trunk, succeed")
                ValError.append("pass")
            else:
                tolog("Add iSCSI Portal,Associated Port Type:Trunk, failed")
                ValError.append("fail")
        else:
            tolog("Add iSCSI Portal,but 'Associated Port Type:Trunk' is grey, So user can't create Trunk Portal")
        time.sleep(1)
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
