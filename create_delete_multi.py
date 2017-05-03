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

class CreateDeleteMulti(unittest.TestCase):


    def test_create_delete_multi(self):
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

        tolog("Start to creating new pool/volume/snapshot/clone,then delete clone/snapshot/volume/pool!")

        sleep(1)

        poolnum0=poolnum1=volnum0=volnum1=snapnum0=snapnum1=clonenum0=clonenum1=0
        validatelist = list()

        # try:
        count = 10
        while count > 1:
            sleep(1)
            print count
            driver.find_element_by_link_text("Pool").click()
            sleep(1)
            driver.find_element_by_xpath("//div[2]/button").click()
            driver.find_element_by_name("name").clear()
            pool_name = random_key(10)
            driver.find_element_by_name("name").send_keys(pool_name)

            raid = random.choice(raid_level)
            if raid == "RAID1":
                disks = random.sample(disklist, 2)
            else:
                disks = random.sample(disklist, 4)
            sleep(1)
            for disk in disks:
                sleep(1)
                driver.find_element_by_xpath("//div[2]/div/div/ul/li[%s]" % (disk)).click()

            sleep(0.5)
            Select(driver.find_element_by_name("raidlevel")).select_by_visible_text(raid)
            sleep(0.5)
            stripsize = random.choice(strip_size)
            Select(driver.find_element_by_name("strip")).select_by_visible_text(stripsize)
            sleep(1)
            sectorsize = random.choice(sector_size)
            Select(driver.find_element_by_name("sector")).select_by_visible_text(sectorsize)
            sleep(1)
            ctrlid = random.choice(Prefer_ctrl)
            driver.find_element_by_xpath("//label[%d]/span" % ctrlid).click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Pool was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Pool %s was added successfully." % pool_name);
                        poolnum0 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
            sleep(1)
            validatelist.append(VerifyWords(driver, (pool_name, raid)))

            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_link_text("View Detail").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, (pool_name, raid, stripsize, sectorsize)))

            driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
            sleep(1)
            driver.find_element_by_link_text("Volume").click()
            sleep(1)
            driver.find_element_by_xpath("//div[2]/button").click()
            sleep(1)

            # Select(driver.find_element_by_name("pool")).select_by_value(pool_name)
            # sleep(1)
            driver.find_element_by_name("volumename").clear()
            volume_name = random_key(15)
            driver.find_element_by_name("volumename").send_keys(volume_name)
            sleep(1)
            # Enable Thin Provision
            driver.find_element_by_xpath("//form/div[4]/div[1]/input").clear()

            driver.find_element_by_xpath("//form/div[4]/div[1]/input").send_keys(volume_capacity)
            sleep(1)
            # driver.find_element_by_css_selector("div.row.m-t-20").click()
            volumesector = random.choice(volume_sector)
            Select(driver.find_element_by_name("sectorsize")).select_by_visible_text(volumesector)
            sleep(1)
            # driver.find_element_by_css_selector("option[value=\"string:1KB\"]").click()
            blocksize = random.choice(block_size)
            Select(driver.find_element_by_name("blocksize")).select_by_visible_text(blocksize)
            sleep(1)
            sync_mode = ["Always", "Standard", "Disabled"]
            syncmode = random.choice(sync_mode)
            Select(driver.find_element_by_name("syncmode")).select_by_visible_text(syncmode)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Volume was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Volume %s was added successfully." % volume_name);
                        volnum0 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
            sleep(1)
            validatelist.append(VerifyWords(driver, (volume_name, blocksize)))

            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_link_text("View Detail").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, (volume_name, blocksize, volumesector)))

            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()  # click v0
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()  # click "snapshot&clone" button
            sleep(1)
            driver.find_element_by_xpath(
                "//pr-button-bar/div/div/div/button[1]").click()  # click 'Create snapshot' button
            sleep(1)
            driver.find_element_by_name("name").clear()
            snapshot_name = random_key(18)
            driver.find_element_by_name("name").send_keys(snapshot_name)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Snapshot was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Snapshot %s was added successfully. " % snapshot_name);
                        snapnum0 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
            a = list()
            a.append(snapshot_name)
            sleep(1)
            validatelist.append(VerifyWords(driver, a))
            sleep(1)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(2)
            driver.find_element_by_link_text("View Detail").click()
            sleep(2)
            validatelist.append(VerifyWords(driver, (snapshot_name, pool_name, volume_name)))

            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            clone_name = random_key(10)
            driver.find_element_by_name("name").send_keys(clone_name)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Clone was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Clone %s was added successfully. " % snapshot_name);
                        clonenum0 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
            sleep(1)
            driver.find_element_by_xpath("//td[2]/a/i").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/a/b").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/ul/li/a").click()

            # driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/a").click()
            # driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/ul/li/a").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, (snapshot_name, clone_name, pool_name, "volume")))

            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            sleep(1)
            driver.find_element_by_xpath("//td[2]/a/i").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[6]/pr-gear-button/div/ul/li[3]/a").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Clone was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Clone %s was deleted successfully." % clone_name);
                        clonenum1 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Snapshot was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Snapshot %s was deleted successfully." % snapshot_name);
                        snapnum1 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(1)
            driver.find_element_by_name("name").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(10):
                try:
                    if re.search(r"^[\s\S]*Volume was deleted successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("volume %s was deleted successfully." % volume_name);
                        volnum1 += 1;
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[3]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            # for i in range(10):
            #     try:
            #         if re.search(r"^[\s\S]*Pool was deleted successfully[\s\S]*$",
            #                      driver.find_element_by_css_selector("BODY").text):
            #             tolog("Pool %s was deleted successfully." % pool_name);
            #             poolnum1 += 1;
            #             break
            #     except:
            #         pass
            #     time.sleep(1)
            # else:
            #     self.fail("time out")

            count -= 1
            print count

        # except:
        #     driver.get_screenshot_as_file("snapshot at " +
        #                                       re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
        #                                           time.time()))) + "create_delete_multi" + "." + "png")
        #     tolog("Error: please refer to the screen-shot in the folder")


        if poolnum0 == poolnum1:
            tolog("Pool created %d, pool deleted %d, this case pass" % (poolnum0, poolnum1))

        else:
            tolog("Pool created %d, pool deleted %d, this case fail" % (poolnum0, poolnum1))
            Failflag = True

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
