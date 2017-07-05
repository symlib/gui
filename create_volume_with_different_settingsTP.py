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
# this is for thinprovision volume
# 2017-7-5
class CreateVolume(unittest.TestCase):


    def test_create_volume(self):
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


        volume_block_size = ['512 Bytes', '1 KB', '2 KB', '4 KB', '8 KB', '16 KB', '32 KB', '64 KB', '128 KB']
        volume_sector = ['512 Bytes', '1 KB', '2 KB', '4 KB']


        raid_level = ["RAID0", "RAID1", "RAID5", "RAID6", "RAID10", "RAID50", "RAID60"]

        tolog("Start to create pool!")
        driver.find_element_by_link_text("Pool").click()

        driver.find_element_by_xpath("//div[2]/button").click()
        sleep(1)

        #poolnum0=poolnum1=volnum0=volnum1=snapnum0=snapnum1=clonenum0=clonenum1=0
        validatelist = list()

        sleep(1)
        driver.find_element_by_name("name").clear()
        pool_name = random_key(10)
        driver.find_element_by_name("name").send_keys(pool_name)
        Select(driver.find_element_by_name("mediatype")).select_by_visible_text("Hard Disk Drive")
        raid = random.choice(raid_level)
        stripsize=random.choice(strip_size)
        sectorsize=random.choice(sector_size)

        if raid == "RAID0":
            disks = random.sample(disklist, 1)
        if raid == "RAID1":
            disks = random.sample(disklist, 2)
        elif raid == "RAID50":
            disks = random.sample(disklist, 6)
        elif raid == "RAID60":
            disks = random.sample(disklist, 8)
        else:
            disks = random.sample(disklist, 4)

        disks.sort()
        verifydisk = list()
        for disk in disks:
            verifydisk.append(int(disk))
        # the verifydisk list will be verified in detail list by removing spaces
        verifydisk.sort()

        disks = verifydisk[::-1]
        # print disks
        # click disk in reverse order to avoid the unapplicable disk selection
        #
        for disk in disks:
            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/div/ul/li[%s]" % (str(disk))).click()

        sleep(1)
        # verifydisk.sort()
        Select(driver.find_element_by_name("raidlevel")).select_by_visible_text(raid)
        sleep(1)
        # sectorsize=random.choice(sector_size)
        Select(driver.find_element_by_name("strip")).select_by_visible_text(stripsize)
        sleep(1)
        Select(driver.find_element_by_name("sector")).select_by_visible_text(sectorsize)
        # sleep(1)
        # ctrlid = random.choice(Prefer_ctrl)

        # driver.find_element_by_xpath("//label[%d]/span" % ctrlid).click()
        sleep(5)

        driver.find_element_by_xpath("//button[@type='submit']").click()
        for i in range(60):
            try:
                if re.search(r"^[\s\S]*Pool was added successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("Pool %s was added successfully." % pool_name);
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

        tolog("Start to create volume")
        sync_mode = ["Always", "Standard", "Disabled"]
        for sector in volume_sector:
            for block in volume_block_size:
                for sync in sync_mode:
                    tolog("Create volume with sector: %s, blocksize: %s, sync mode: %s" %(sector,block,sync))
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
                    #volumesector = random.choice(volume_sector)
                    Select(driver.find_element_by_name("sectorsize")).select_by_visible_text(sector)
                    sleep(2)
                    # driver.find_element_by_css_selector("option[value=\"string:1KB\"]").click()
                    #blocksize = random.choice(block_size)
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

                    validatelist.append(VerifyWords(driver, (volume_name,pool_name, block)))
                    time.sleep(2)
                    driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                    time.sleep(2)

                    driver.find_element_by_link_text("View Detail").click()
                    sleep(2)
                    validatelist.append(VerifyWords(driver, (volume_name, "Exported", pool_name, block, sector)))

                    driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
                    time.sleep(3)
                    driver.find_element_by_css_selector("a > small.ng-binding").click()
                    time.sleep(2)
                    validatelist.append(VerifyWords(driver, ("Enabled", "Exported", volume_name,pool_name, block, sector)))
                    sleep(2)
                    driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a").click()
                    sleep(4)
                    driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
                    sleep(2)
                    driver.find_element_by_xpath("//button[@type='button']").click()
                    sleep(2)
                    driver.find_element_by_name("name").click()
                    sleep(2)
                    driver.find_element_by_name("name").clear()
                    driver.find_element_by_name("name").send_keys("confirm")
                    sleep(2)
                    driver.find_element_by_xpath("//button[@type='submit']").click()

                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was deleted successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("volume %s was deleted successfully." %volume_name);

                                break
                        except:
                            Failflag = True
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

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