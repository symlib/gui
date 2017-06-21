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

class FCPortMod(unittest.TestCase):
    def test_fc_mod(self):
        ValError = []
        Failflag = False
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        tolog("Start to Modify FC mgmt ---> Port settings")
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("FC Management").click()
        time.sleep(1)
        driver.find_element_by_link_text("Port").click()
        time.sleep(2)
        port_entrys = driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")
        port_select = random.randint(2,len(port_entrys)+1)
        driver.find_element_by_xpath("//table[2]/tbody/tr[%d]/td[1]/input" % port_select).click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@title='View FC Ports Settings']").click()
        time.sleep(1)
        cur_speed = random.choice(['Auto','4 Gb/s','8 Gb/s','16 Gb/s'])
        config_topo = random.choice(["Auto","N-Port","NL-Port"])
        alpa = random.randint(0,255)
        Select(driver.find_element_by_name("linkSpeed")).select_by_visible_text(cur_speed)
        Select(driver.find_element_by_xpath("//form/div[2]/div/select")).select_by_visible_text(config_topo)
        #Select(driver.find_element_by_name("topology")).select_by_visible_text(config_topo)
        driver.find_element_by_name("hardalpa").clear()
        driver.find_element_by_name("hardalpa").send_keys(alpa)
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("confirm")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)
        tolog("Start to verify settings")
        driver.find_element_by_xpath("//table[2]/tbody/tr[%d]/td[1]/input" % port_select).click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@title='View FC Ports Information']").click()
        time.sleep(1)
        if cur_speed in driver.find_element_by_xpath("//dl[7]/dd[1]").text:
            ValError.append("pass")
            tolog("Configured Link Speed:PASS")
        else:
            ValError.append("fail")
            tolog("Configured Link Speed:FAIL")
        if config_topo in driver.find_element_by_xpath("//dl[7]/dd[2]").text:
            ValError.append("pass")
            tolog("Configured Topology:PASS")
        else:
            ValError.append("fail")
            tolog("Configured Topology:FAIL")
        if str(alpa) in driver.find_element_by_xpath("//dl[8]/dd").text:
            ValError.append("pass")
            tolog("Hard ALPA:PASS")
        else:
            ValError.append("fail")
            tolog("Hard ALPA:FAIL")

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
