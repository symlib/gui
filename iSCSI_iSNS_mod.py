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

class ISCSIISNSMod(unittest.TestCase):
    def test_iscsi_isns_mod(self):
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
        driver.find_element_by_link_text("iSNS").click()
        time.sleep(2)
        tolog("Start to Modify iSCSI iSNS setting")
        driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]/input").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//button[@title='Modify iSCSI ISNS Settings']").click()
        time.sleep(2)
        if driver.find_element_by_xpath("//form/div[2]/div[1]/label/input").is_selected():
            driver.find_element_by_xpath("//form/div[2]/div[1]/label/input").click()
            time.sleep(0.5)
            isns_status = "Disable"
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(4)
            tolog("Start to verify modifications")
            if str(driver.find_element_by_xpath("//table/tbody").text.split("\n")[0]).split()[3] == isns_status:
                ValError.append("pass")
                tolog("Modify iSNS Status to Disable, PASS")
            else:
                ValError.append("fail")
                tolog("Modify iSNS Status to Disable, FAIL")
        else:
            driver.find_element_by_xpath("//form/div[2]/div[1]/label/input").click()
            isns_status = "Enable"
            server_port = random.randint(1,65535)
            server_ip = "%d.%d.%d.%d" % (
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            tolog("Set server port = %d" % server_port)
            tolog("Set server IP = %s" % server_ip)
            driver.find_element_by_name("serverport").clear()
            time.sleep(0.5)
            driver.find_element_by_name("serverport").send_keys(str(server_port))
            time.sleep(1)
            driver.find_element_by_name("serverip").clear()
            time.sleep(0.5)
            driver.find_element_by_name("serverip").send_keys(server_ip)
            time.sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(4)
            tolog("Start to verify modifications")
            if str(driver.find_element_by_xpath("//table/tbody").text.split("\n")[0]).split()[3] == isns_status:
                ValError.append("pass")
                tolog("Modify iSNS Status to Enable, PASS")
            else:
                ValError.append("fail")
                tolog("Modify iSNS Status to Enable, FAIL")
            if str(driver.find_element_by_xpath("//table/tbody").text.split("\n")[0]).split()[4] == server_ip:
                ValError.append("pass")
                tolog("Modify iSNS Server IP, PASS")
            else:
                ValError.append("fail")
                tolog("Modify iSNS Server IP, FAIL")
            if str(driver.find_element_by_xpath("//table/tbody").text.split("\n")[0]).split()[-1] == str(server_port):
                ValError.append("pass")
                tolog("Modify iSNS Server Port, PASS")
            else:
                ValError.append("fail")
                tolog("Modify iSNS Server Port, FAIL")
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
