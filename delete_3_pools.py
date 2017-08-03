# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, random
from login_ds import loginFirefox
from login_ds import loginIE
from VerifyWords import VerifyWords
from time import sleep
from to_log import tolog
from namegenerator import random_key

import time
Pass="'result': 'p'"
Fail="'result': 'f'"

class DeletePool(unittest.TestCase):


    def test_delete_pool(self):
        Failflag = False
        self.driver = loginFirefox()
        # self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver




        sleep(1)

        validatelist = list()
        try:

            sleep(1)

            tolog("Delete pool from pool list")
            driver.find_element_by_xpath("//div[2]/div/ul/li[3]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Pool was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Pool was deleted successfully.");

                        break
                except:
                    Failflag = True
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            tolog("Delete pool from gear button")

            sleep(1)
            driver.find_element_by_xpath("//tr[2]/td[8]/pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[2]/td[8]/pr-gear-button/div/ul/li[2]/a").click()
            sleep(1)
            driver.find_element_by_name("name").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Pool was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Pool was deleted successfully.");
                        break
                except:
                    Failflag = True
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            tolog("Delete pool from pool page")
            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[3]/a/span").click()
            # sleep(1)
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/pr-button-bar/div/div/div/button[1] ").click()

            sleep(1)
            driver.find_element_by_name("name").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Pool was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Pool was deleted successfully.");
                        break
                except:
                    Failflag = True
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
        except:
            Failflag = True
            driver.get_screenshot_as_file("snapshot at " +
                                          re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                              time.time()))) + "create_delete_multi" + "." + "png")
            tolog("Error: please refer to the screen-shot in the folder")

        for val in validatelist:
            if val:
                Failflag = True
                break

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
