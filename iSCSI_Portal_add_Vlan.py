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
    def test_iscsi_portal_add_vlan(self):
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
        driver.find_element_by_link_text("Portal").click()
        time.sleep(2)
        if "No iSCSI Portal detected." in driver.find_element_by_xpath("//table/tbody").text:
            portal_entry1 = 0
        else:
            portal_entry1 = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        ctrl_id = []
        port_id = []
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        time.sleep(3)
        if driver.find_element_by_xpath("//form/div[1]/div/label[3]/input").is_enabled():
            driver.find_element_by_xpath("//form/div[1]/div/label[3]/input").click()
            time.sleep(1)
            if driver.find_element_by_xpath("//form/div[2]/div/label[1]/input").is_enabled():
                ctrl_id.append("1")
            if driver.find_element_by_xpath("//form/div[2]/div/label[2]/input").is_enabled():
                ctrl_id.append("2")
            if driver.find_element_by_xpath("//form/div[3]/div/label[1]/input").is_enabled():
                port_id.append("1")
            if driver.find_element_by_xpath("//form/div[3]/div/label[2]/input").is_enabled():
                port_id.append("2")
            driver.find_element_by_xpath("//form/div[2]/div/label[%s]/input" % random.choice(ctrl_id)).click()
            time.sleep(1)
            driver.find_element_by_xpath("//form/div[3]/div/label[%s]/input" % random.choice(port_id)).click()
            time.sleep(1)
            vlan_tag = random.randint(1,4094)
            driver.find_element_by_name("vlantag").clear()
            time.sleep(0.5)
            driver.find_element_by_name("vlantag").send_keys(vlan_tag)
            time.sleep(1)
            TCP_Port_number = random.randint(0, 65535)
            driver.find_element_by_name("tcpportnumber").clear()
            time.sleep(0.5)
            driver.find_element_by_name("tcpportnumber").send_keys(TCP_Port_number)
            time.sleep(0.5)
            IP_Type = random.choice(["IPv4", "IPv6"])
            Select(driver.find_element_by_name("ip_type")).select_by_visible_text(IP_Type)
            time.sleep(1)
            driver.find_element_by_xpath("//form/div[7]/div[1]/label/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(5)
            portal_entry2 = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
            if portal_entry2 > portal_entry1:
                tolog("Add iSCSI Portal,Associated Port Type:Vlan, succeed")
                ValError.append("pass")
            else:
                tolog("Add iSCSI Portal,Associated Port Type:Vlan, failed")
                ValError.append("fail")
        else:
            tolog("Add iSCSI Portal,but 'Associated Port Type:Vlan' is grey, So user can't create Vlan Portal")
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
