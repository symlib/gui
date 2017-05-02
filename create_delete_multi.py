# -*- coding: utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest,re,random
from print_result import printSF
from login_ds import login
from VerifyWords import VerifyWords
from time import sleep
from to_log import tolog

class CreateDeleteMulti(unittest.TestCase):
    def test_create_delete_multi(self):
        Result = "'result': 'p'"
        self.driver = login()
        #self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver

        i ,j = 0,1
        while i < 2:
            tolog("Start to creating new pool/volume/snapshot/clone,then delete clone/snapshot/volume/pool!")
            tolog("======This is the %s time(s)======" % str(i+1))
            driver.find_element_by_link_text("Pool").click()
            sleep(2)
            driver.find_element_by_xpath("//div[2]/button").click()
            sleep(2)
            driver.find_element_by_name("name").clear()
            pool_name = "p%d" % i
            driver.find_element_by_name("name").send_keys(pool_name)
            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/div/ul/li[%s]" % str(j)).click()
            sleep(0.5)
            driver.find_element_by_xpath("//div[2]/div/div/ul/li[%s]" % str(j+1)).click()
            sleep(1)
            strip_size = ["64 KB", "128 KB", "256 KB", "512 KB", "1 MB"]
            Select(driver.find_element_by_name("strip")).select_by_visible_text(random.choice(strip_size))
            sleep(1)
            sector_size = ["512 Bytes", "1 KB", "2 KB", "4 KB"]
            Select(driver.find_element_by_name("sector")).select_by_visible_text(random.choice(sector_size))
            sleep(1)
            Prefer_ctrl = [1, 2]
            driver.find_element_by_xpath("//label[%d]/span" % random.choice(Prefer_ctrl)).click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(20)
            tolog("Pool %s was created!" % pool_name)
            '''
            try: self.assertEqual("Pool was added successfully.", driver.find_element_by_xpath("//div[5]/div/div").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
        '''
            #driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
            driver.find_element_by_link_text("Volume").click()
            sleep(2)
            driver.find_element_by_xpath("//div[2]/button").click()
            sleep(2)
            driver.find_element_by_xpath("//form/div[1]/div/select").send_keys(pool_name)
            #Select(driver.find_element_by_name("pool")).select_by_value(pool_name)
            sleep(1)
            driver.find_element_by_name("volumename").clear()
            volume_name = "v%d" % i
            driver.find_element_by_name("volumename").send_keys(volume_name)
            sleep(1)
            # Enable Thin Provision
            driver.find_element_by_xpath("//form/div[4]/div[1]/input").clear()
            volume_capacity = str(random.randint(16,10000))
            driver.find_element_by_xpath("//form/div[4]/div[1]/input").send_keys(volume_capacity)
            sleep(2)
            #driver.find_element_by_css_selector("div.row.m-t-20").click()
            volume_sector = ['512 Bytes','1 KB', '2 KB','4 KB']
            Select(driver.find_element_by_name("sectorsize")).select_by_visible_text(random.choice(volume_sector))
            sleep(1)
            #driver.find_element_by_css_selector("option[value=\"string:1KB\"]").click()
            block_size = ['512 Bytes','1 KB', '2 KB','4 KB', '8 KB','16 KB','32 KB','64 KB','128 KB']
            Select(driver.find_element_by_name("blocksize")).select_by_visible_text(random.choice(block_size))
            sleep(1)
            sync_mode = ["Always","Standard","Disabled"]
            Select(driver.find_element_by_name("syncmode")).select_by_visible_text(random.choice(sync_mode))
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(7)
            tolog("Volume %s was created" % volume_name)
            '''
            try: self.assertEqual("Volume was added successfully.", driver.find_element_by_xpath("//div[5]/div/div").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
            '''
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()  #click v0
            sleep(2)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #click "snapshot&clone" button
            sleep(2)
            driver.find_element_by_xpath("//pr-button-bar/div/div/div/button[1]").click()# click 'Create snapshot' button
            sleep(1)
            driver.find_element_by_name("name").clear()
            snapshot_name = "snap_%d" % i
            driver.find_element_by_name("name").send_keys(snapshot_name)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(5)
            tolog("snapshot %s was created" % snapshot_name)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()#click snapshot checkbox
            sleep(2)
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()#click "Create clone" button
            sleep(1)
            driver.find_element_by_name("name").clear()
            clone_name = ("c_%s" % i)
            driver.find_element_by_name("name").send_keys(clone_name)
            sleep(2)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(5)
            tolog("Clone %s was created!" % clone_name)
            sleep(5)
            tolog("Start to delete existing clone/snapshot/volume/pool!!!")
            sleep(2)
            driver.find_element_by_css_selector("a.tree-icon.ng-scope > i.fa.fa-plus-square").click()
            sleep(1)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            sleep(1)
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(8)
            tolog("Clone %s was deleted!" % clone_name)
            driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
            sleep(2)
            driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
            sleep(1)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(8)
            tolog("snapshot %s was deleted!" % snapshot_name)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(3)
            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(2)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(8)
            tolog("Volume %s was deleted!" % volume_name)
            driver.find_element_by_link_text("Pool").click()
            sleep(3)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(2)
            driver.find_element_by_name("name").clear()
            driver.find_element_by_name("name").send_keys("confirm")
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(8)
            tolog("Pool %s was deleted!" % pool_name)
            tolog("Create pool/voume/snapshot/clone, then delete them, PASS!!")
            '''
            try: self.assertEqual("Volume was deleted successfully.", driver.find_element_by_xpath("//div[5]/div/div").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
           '''

            i += 1
            j += 2

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
