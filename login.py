# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Login(unittest.TestCase):
    def setUp(self):
        fp = webdriver.FirefoxProfile("C:\Users\Jacky\AppData\Roaming\Mozilla\Firefox\Profiles\\gzr3f98b.ds")
        fp.accept_untrusted_certs = True
        #driver = webdriver.Firefox(firefox_profile=fp)
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(30)
        self.base_url = "https://10.84.2.164/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login(self):

        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//input[@name='username']").clear()
        driver.find_element_by_xpath("//input[@name='username']").send_keys("administrator")
        driver.find_element_by_xpath("//input[@name='password']").clear()
        driver.find_element_by_xpath("//input[@name='password']").send_keys("password")
        driver.find_element_by_xpath("//button[@type='submit']").click()
    
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
