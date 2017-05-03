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

class DeleteClone(unittest.TestCase):


    def test_create_delete_clone(self):
        Failflag = False
        self.driver = loginFirefox()
        # self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver

        strip_size = ["64 KB", "128 KB", "256 KB", "512 KB", "1 MB"]
        sector_size = ["512 Bytes", "1 KB", "2 KB", "4 KB"]

        Prefer_ctrl = [1, 2]
        disklist = ["1", "3", "4", "5", "6", "8", "9", "10", "11", "12"]

        volume_capacity = str(random.randint(16, 10000))
        block_size = ['512 Bytes', '1 KB', '2 KB', '4 KB', '8 KB', '16 KB', '32 KB', '64 KB', '128 KB']
        volume_sector = ['512 Bytes', '1 KB', '2 KB', '4 KB']

        raid_level = ["RAID1", "RAID5", "RAID6"]


        sleep(1)

        validatelist = list()
        try:
            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            driver.find_element_by_xpath("//td[2]/a/i").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/a").click()
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/ul/li[3]/a").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Clone was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Clone was deleted successfully.");

                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            #

        except:
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
