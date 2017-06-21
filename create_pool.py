# -*- coding: utf-8 -*-
# !/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, re, random,time
from login_ds import loginFirefox
from login_ds import loginIE
from VerifyWords import VerifyWords
from to_log import tolog
from namegenerator import random_key

Pass="'result': 'p'"
Fail="'result': 'f'"

class CreatePool(unittest.TestCase):
    def test_create_pool(self):
        Failflag = False
        ValError = []
        self.driver = loginFirefox()
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        strip_size = ["64 KB", "128 KB", "256 KB", "512 KB", "1 MB"]
        sector_size = ["512 Bytes", "1 KB", "2 KB", "4 KB"]
        Prefer_ctrl = [1, 2]
        disklist = []#unconfigured pd list
        disks = []#selected pd list
        raid = ""#selected raid level
        driver.find_element_by_link_text("Device").click()
        time.sleep(2)
        driver.find_element_by_link_text("Physical Drive").click()
        time.sleep(5)
        if "There is no" in driver.find_element_by_xpath("//table[2]/tbody").text:
            tolog("No PD in enclosure")
            ValError.append("pass")
        else:
            pd_lines = len(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n"))
            for i in range(pd_lines):
                if i % 2 != 0:
                    if "Unconfigured" in driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")[i] \
                            and "HDD" in driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")[i]:
                        disklist.append(str(driver.find_element_by_xpath("//table[2]/tbody").text.split("\n")[i-1]))
            tolog("Unconfigured HDD PD is : %s" % str(disklist))
            time.sleep(1)
            if disklist != []:
                driver.find_element_by_link_text("Pool").click()
                time.sleep(2)
                tolog("Start to Create Pool........")
                driver.find_element_by_xpath("//button[@title='Create New Pool']").click()
                time.sleep(3)
                driver.find_element_by_name("name").clear()
                pool_name = random_key(10)
                driver.find_element_by_name("name").send_keys(pool_name)
                if len(disklist) == 1:
                    raid = "RAID0"
                elif  len(disklist) == 2:
                    raid = random.choice(["RAID0","RAID1"])
                elif len(disklist) == 3:
                    raid = random.choice(["RAID0","RAID5"])
                elif len(disklist) == 4:
                    raid = random.choice(["RAID0", "RAID5","RAID10","RAID6"])
                elif len(disklist) == 5:
                    raid = random.choice(["RAID0", "RAID5", "RAID6"])
                elif len(disklist) == 6:
                    raid = random.choice(["RAID0", "RAID5", "RAID10", "RAID6","RAID50"])
                elif len(disklist) == 7:
                    raid = random.choice(["RAID0", "RAID5", "RAID6", "RAID50"])
                elif len(disklist) == 8:
                    raid = random.choice(["RAID0", "RAID5", "RAID6", "RAID10","RAID50","RAID60"])
                elif len(disklist) >= 9 and len(disklist) % 2 != 0 :
                    raid = random.choice(["RAID0", "RAID5", "RAID6", "RAID50", "RAID60"])
                elif len(disklist) > 9 and len(disklist) % 2 == 0:
                    raid = random.choice(["RAID0", "RAID5", "RAID6", "RAID10","RAID50", "RAID60"])
                #print "raid ,is,,,,===",raid, type(raid)
                if raid == "RAID0":
                    disks = random.sample(disklist, 1)
                elif raid == "RAID1":
                    disks = random.sample(disklist, 2)
                elif raid == "RAID5":
                    disks = random.sample(disklist, 3)
                elif raid == "RAID50":
                    disks = random.sample(disklist, 6)
                elif raid == "RAID60":
                    disks = random.sample(disklist, 8)
                elif raid == "RAID10" or "RAID6":
                    disks = random.sample(disklist, 4)
                disks = [int(x) for x in disks]
                disks.sort(reverse=True)
                for line in disks:
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[2]/div[1]/div[1]/ul/li[%d]" % (line)).click()
                time.sleep(1)
                #Select(driver.find_element_by_xpath("//form/div[5]/div/select")).select_by_visible_text(raid)
                #Select(driver.find_element_by_name("raidlevel")).select_by_visible_text(raid)
                Select(driver.find_element_by_xpath("//select[@name='raidlevel']")).select_by_visible_text(raid)
                time.sleep(0.5)
                stripsize = random.choice(strip_size)
                Select(driver.find_element_by_name("strip")).select_by_visible_text(stripsize)
                time.sleep(1)
                sectorsize = random.choice(sector_size)
                Select(driver.find_element_by_name("sector")).select_by_visible_text(sectorsize)
                time.sleep(1)
                ctrlid = random.choice(Prefer_ctrl)
                driver.find_element_by_xpath("//label[%d]/span" % ctrlid).click()
                time.sleep(1)
                driver.find_element_by_xpath("//button[@type='submit']").click()
                for i in range(60):
                    try:
                        if re.search(r"^[\s\S]*Pool was added successfully.[\s\S]*$",
                                     driver.find_element_by_css_selector("BODY").text):
                            tolog("Pool %s was added successfully." % pool_name);
                            break
                    except:
                        tolog(driver.find_element_by_xpath("//body/div/div/div[5]/div/div").text)
                        time.sleep(1)
                        driver.get_screenshot_as_file("create pool" +
                                                      re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                                          time.time()))) + "create_pool" + "." + "png")
                        tolog("Error: please refer to the screen-shot in the folder")
                        break
                else:
                    self.fail("time out")
                if driver.find_element_by_link_text(pool_name).is_displayed():
                    time.sleep(5)
                    driver.find_element_by_link_text(pool_name).click()
                    time.sleep(3)
                    #driver.find_element_by_link_text("Expand Detail Information").click()
                    driver.find_element_by_xpath("//a/small[1]").click()
                    time.sleep(3)
                    if driver.find_element_by_xpath("//dl[4]/dd").text == raid:
                        ValError.append("pass")
                        tolog("Verify Pool raid level is correct")
                    else:
                        ValError.append("fail")
                        tolog("Verify Pool raid level is wrong")
                    if ("Controller %s" % ctrlid) == driver.find_element_by_xpath("//dl[5]/dd/span[1]").text:
                        ValError.append("pass")
                        tolog("Verify Pool preferred ctrl is correct")
                    else:
                        tolog("Verify Preferred Controller is wrong")
                        ValError.append("fail")
                    if str(driver.find_element_by_xpath("//dl[7]/dd").text) == stripsize:
                        ValError.append("pass")
                        tolog("Verify Pool stripe size is correct")
                    else:
                        ValError.append("fail")
                        tolog("Verify Pool stripe size is wrong")
                    if str(driver.find_element_by_xpath("//dl[8]/dd").text) == sectorsize:
                        ValError.append("pass")
                        tolog("Verify Pool sector size is correct")
                    else:
                        ValError.append("fail")
                        tolog("Verify Pool sector size is wrong")
            else:
                tolog("No Unconfigured PD")
                ValError.append("pass")
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
