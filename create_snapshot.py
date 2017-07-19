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
shortterm=1
mediumterm=3
longterm=8
class CreateSnapshot(unittest.TestCase):


    def test_create_snapshot(self):
        Failflag = False
        self.driver = loginFirefox()
        # self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver


        sleep(shortterm)


        validatelist = list()
        try:
            tolog("Create snapshot from volume")
            driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
            sleep(shortterm)
            driver.find_element_by_link_text("Volume").click()

            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()  # click v0
            sleep(shortterm)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()  # click "snapshot&clone" button
            sleep(shortterm)
            driver.find_element_by_xpath(
                "//pr-button-bar/div/div/div/button[1]").click()  # click 'Create snapshot' button
            sleep(shortterm)
            driver.find_element_by_name("name").clear()
            snapshot_name = random_key(18)
            driver.find_element_by_name("name").send_keys(snapshot_name)
            sleep(shortterm)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Snapshot was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Snapshot %s was added successfully. " %snapshot_name);

                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")


            sleep(longterm)
            driver.find_element_by_link_text("Volume").click()
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)

            driver.find_element_by_link_text("View Detail").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot " + snapshot_name})))

            sleep(shortterm)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(mediumterm)
            driver.find_element_by_css_selector("a > small.ng-binding").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot " + snapshot_name})))


            tolog("Export and Un-export snapshot")
            sleep(longterm)
            driver.find_element_by_link_text("Volume").click()
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)
            driver.find_element_by_link_text("Snapshot & Clone").click()
            sleep(2)
            for i in range(2):
                status=False

                if re.search("Un-Exported", driver.find_element_by_css_selector("BODY").text):
                    status=True

                sleep(shortterm)
                driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                sleep(shortterm)
                if status:
                    driver.find_element_by_link_text("Export Snapshot").click()
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Snapshot was exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Snapshot was exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

                else:
                    driver.find_element_by_link_text("Un-export Snapshot").click()
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Snapshot was un-exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Snapshot was un-exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")


            tolog("Modify snapshot")
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)
            driver.find_element_by_link_text("Modify Snapshot").click()
            sleep(shortterm)
            driver.find_element_by_name("name").clear()
            snapshot_name = random_key(20)
            driver.find_element_by_name("name").send_keys(snapshot_name)
            sleep(shortterm)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            sleep(mediumterm)
            validatelist.append(VerifyWords(driver,({snapshot_name})))
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Snapshot was changed successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Snapshot was changed successfully..");
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            sleep(longterm)
            driver.find_element_by_link_text("Volume").click()
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)

            driver.find_element_by_link_text("View Detail").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot " + snapshot_name})))

            sleep(shortterm)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(mediumterm)
            driver.find_element_by_css_selector("a > small.ng-binding").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot " + snapshot_name})))


            tolog("Create snapshot from gear button")
            sleep(shortterm)
            driver.find_element_by_link_text("Volume").click()
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)
            driver.find_element_by_link_text("Snapshot & Clone").click()
            sleep(shortterm)

            driver.find_element_by_xpath("//button[@type='button']").click()
            sleep(shortterm)
            driver.find_element_by_name("name").clear()
            snapshot_name = random_key(18)
            driver.find_element_by_name("name").send_keys(snapshot_name)
            sleep(shortterm)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Snapshot was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Snapshot %s was added successfully. " %snapshot_name);

                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            sleep(longterm)
            driver.find_element_by_link_text("Volume").click()
            sleep(shortterm)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(shortterm)

            driver.find_element_by_link_text("View Detail").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot "+snapshot_name})))

            sleep(shortterm)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(mediumterm)
            driver.find_element_by_css_selector("a > small.ng-binding").click()
            sleep(shortterm)
            validatelist.append(VerifyWords(driver, ({"Snapshot "+snapshot_name})))


        except:
            driver.get_screenshot_as_file("snapshot at " +
                                          re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                              time.time()))) + "create_delete_multi" + "." + "png")
            tolog("Error: please refer to the screen-shot in the folder")
            Failflag = True

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
