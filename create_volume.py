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
from to_log import tolog
from namegenerator import random_key
import time
Pass="'result': 'p'"
Fail="'result': 'f'"
from time import sleep

class CreateVolume(unittest.TestCase):
    def test_create_volume(self):
        Failflag = False

        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        #volume_capacity = str(random.randint(1, 1000000))
        block_size = ['512 Bytes', '1 KB', '2 KB', '4 KB', '8 KB', '16 KB', '32 KB', '64 KB', '128 KB']
        volume_sector = ['512 Bytes', '1 KB', '2 KB', '4 KB']
        raid_level = ["RAID1", "RAID5", "RAID6"]
        tolog("Start to create volume.")
        validatelist = []
        block=random.choice(block_size)
        sector=random.choice(volume_sector)
        sync_mode = ["Always", "Standard", "Disabled"]
        sync=random.choice(sync_mode)
        volume_capacity = str(random.randint(1, 10000))
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
        sleep(2)
        driver.find_element_by_link_text("Volume").click()
        sleep(2)
        driver.find_element_by_xpath("//div[2]/button").click()
        sleep(2)
        driver.find_element_by_name("volumename").clear()
        volume_name = random_key(10)
        sleep(2)
        driver.find_element_by_name("volumename").send_keys(volume_name)
        sleep(2)

        driver.find_element_by_xpath("//form/div[4]/div[1]/input").clear()
        # Enable Thin Provision
        sleep(2)
        driver.find_element_by_xpath("//input[@type='checkbox']").click()
        sleep(2)
        driver.find_element_by_xpath("//form/div[4]/div[1]/input").send_keys(volume_capacity)
        sleep(2)
        # driver.find_element_by_css_selector("div.row.m-t-20").click()
        # volumesector = random.choice(volume_sector)
        Select(driver.find_element_by_name("sectorsize")).select_by_visible_text(sector)
        sleep(2)
        # driver.find_element_by_css_selector("option[value=\"string:1KB\"]").click()
        # blocksize = random.choice(block_size)
        Select(driver.find_element_by_name("blocksize")).select_by_visible_text(block)
        sleep(2)

        Select(driver.find_element_by_name("syncmode")).select_by_visible_text(sync)

        sleep(2)

        driver.find_element_by_xpath("//button[@type='submit']").click()
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*Volume was added successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("Volume %s was added successfully." % volume_name);
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

        # validatelist.append(VerifyWords(driver, (volume_name,block)))
        # time.sleep(2)
        # driver.find_element_by_xpath("//pr-gear-button/div/a").click()
        # time.sleep(2)
        #
        # driver.find_element_by_link_text("View Detail").click()
        # sleep(2)
        # validatelist.append(VerifyWords(driver, (volume_name, "Exported",block, sector)))
        #
        # driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
        # time.sleep(3)
        # driver.find_element_by_css_selector("a > small.ng-binding").click()
        # time.sleep(2)
        # validatelist.append(VerifyWords(driver, ("Enabled", "Exported", volume_name,block, sector)))

        for val in validatelist:
            if val:
                Failflag=True
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
