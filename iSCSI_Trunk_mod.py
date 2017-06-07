# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random, time
# from print_result import printSF
from login_ds import loginFirefox
from VerifyWords import VerifyWords
from to_log import tolog

Pass = "'result': 'p'"
Fail = "'result': 'f'"


class ISCSITrunkMod(unittest.TestCase):
    def test_iscsi_trunk_mod(self):
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
        if "No iSCSI Trunk detected." in driver.find_element_by_xpath("//table/tbody").text:
            tru_list_1 = 0
            tolog("No Trunk entry need to modify")
            ValError.append("pass")
        else:
            tru_list_1 = len(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        time.sleep(2)
        mesg = "To create trunk, please delete iSCSI Portal(s) first. At least TWO unused ports are required to create trunk."
        if mesg in driver.find_element_by_xpath("//div[4]/div/div/div").text:
            tolog(mesg)
            ValError.append("pass")
        else:
            temp = []
            if driver.find_element_by_xpath("//form/div[1]/div/label[1]").is_enabled():
                temp.append("1")
            if driver.find_element_by_xpath("//form/div[1]/div/label[2]").is_enabled():
                temp.append("2")
            trunk_type = random.choice(temp)
            driver.find_element_by_xpath("//form/div[1]/div/label[%s]" % trunk_type).click()
            time.sleep(1)
            del temp[:]
            if driver.find_element_by_xpath("//form/div[2]/div/label[1]").is_enabled():
                temp.append("1")
            if driver.find_element_by_xpath("//form/div[2]/div/label[2]").is_enabled():
                temp.append("2")
            ctrl_id = random.choice(temp)
            driver.find_element_by_xpath("//form/div[2]/div/label[%s]" % ctrl_id).click()
            time.sleep(1)
            del temp[:]
            if driver.find_element_by_xpath("//form/div[3]/div/label[1]").is_enabled():
                temp.append("1")
            if driver.find_element_by_xpath("//form/div[3]/div/label[2]").is_enabled():
                temp.append("2")
            master_port = random.choice(temp)
            driver.find_element_by_xpath("//form/div[3]/div/label[%s]" % master_port).click()
            time.sleep(1)
            temp.remove(master_port)
            slave_port = temp[0]
            if driver.find_element_by_xpath("//form/div[4]/div/label[%s]" % slave_port).is_enabled():
                pass
            else:
                tolog("Add iSCSI Trunk, Slave Port has error.")
                ValError.append("fail")
            driver.find_element_by_xpath("(//button[@type='submit'])").click()
            time.sleep(4)
            if len(driver.find_element_by_xpath("//table/tbody").text.split("\n")) > tru_list_1:
                tolog("iSCSI Trunk was added successfully")
                ValError.append("pass")
            else:
                tolog("Add iSCSI Trunk has error")
                ValError.append("fail")
            time.sleep(2)
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
