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

class CreatePool(unittest.TestCase):


    def test_create_pool(self):
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
        #disklist = [1, 3, 4, 5, 6, 8, 9, 10, 11, 12]

        volume_capacity = str(random.randint(16, 10000))
        block_size = ['512 Bytes', '1 KB', '2 KB', '4 KB', '8 KB', '16 KB', '32 KB', '64 KB', '128 KB']
        volume_sector = ['512 Bytes', '1 KB', '2 KB', '4 KB']

        raid_level = ["RAID0", "RAID1", "RAID5", "RAID6","RAID1", "RAID5", "RAID6"]

        tolog("Start to creating new pool/volume/snapshot/clone,then delete clone/snapshot/volume/pool!")
        driver.find_element_by_link_text("Pool").click()

        driver.find_element_by_xpath("//div[2]/button").click()
        sleep(1)

        #poolnum0=poolnum1=volnum0=volnum1=snapnum0=snapnum1=clonenum0=clonenum1=0
        validatelist = list()
        try:
            sleep(1)
            driver.find_element_by_name("name").clear()
            pool_name = random_key(10)
            driver.find_element_by_name("name").send_keys(pool_name)
            Select(driver.find_element_by_name("mediatype")).select_by_visible_text("Hard Disk Drive")
            raid = random.choice(raid_level)


            if raid == "RAID1":
                disks = random.sample(disklist, 2)
            elif raid=="RAID50":
                disks = random.sample(disklist, 6)
            elif raid == "RAID60":
                disks = random.sample(disklist, 8)
            else:
                disks = random.sample(disklist, 4)

            disks.sort()
            disks=disks[::-1]
            print disks
            for disk in disks:
                sleep(1)
                driver.find_element_by_xpath("//div[2]/div/div/ul/li[%s]" % (disk)).click()

            sleep(0.5)
            Select(driver.find_element_by_name("raidlevel")).select_by_visible_text(raid)
            stripsize=random.choice(strip_size)
            Select(driver.find_element_by_name("strip")).select_by_visible_text(stripsize)
            sleep(1)
            sectorsize=random.choice(sector_size)
            Select(driver.find_element_by_name("sector")).select_by_visible_text(sectorsize)
            sleep(1)
            ctrlid = random.choice(Prefer_ctrl)

            driver.find_element_by_xpath("//label[%d]/span" % ctrlid).click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Pool was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Pool %s was added successfully." %pool_name);
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            validatelist.append(VerifyWords(driver, (pool_name, raid)))

            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            driver.find_element_by_link_text("View Detail").click()
            sleep(2)
            validatelist.append(VerifyWords(driver, (pool_name, raid, stripsize, sectorsize)))

        except:
            driver.get_screenshot_as_file("snapshot at " +
                                          re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                              time.time()))) + "create_delete_multi" + "." + "png")
            tolog("Error: please refer to the screen-shot in the folder")

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
