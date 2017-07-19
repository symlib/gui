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

class CreateClone(unittest.TestCase):
    def test_create_clone(self):
        Failflag = False
        self.driver = loginFirefox()
        # self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        validatelist = []
        try:
            tolog("Start to create clone from snapshot list")

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
            sleep(1)
            driver.find_element_by_name("name").clear()
            clone_name = random_key(10)
            driver.find_element_by_name("name").send_keys(clone_name)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            for i in range(60):
                try:
                    if re.search(r"^[\s\S]*Clone was added successfully.[\s\S]*$",
                                 driver.find_element_by_css_selector("BODY").text):
                        tolog("Clone %s was added successfully. " %clone_name);
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")

            driver.find_element_by_xpath("//td[2]/a/i").click()
            # click plus sign to get the clone name
            sleep(1)
            tolog("Verify the clone name in clone list")
            validatelist.append(VerifyWords(driver, ({clone_name})))
            sleep(1)

            # click volume to show latest clone for the volume
            tolog("Verify the latest clone name in volume page")
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            driver.find_element_by_xpath("//a/small").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, ({clone_name})))

            # to create clone from gear button
            driver.find_element_by_xpath("//button[4]").click()
            sleep(1)
            tolog("Start to create clone from gear button")
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_link_text("Create Clone").click()
            sleep(1)
            clone_name = random_key(15)
            driver.find_element_by_name("name").send_keys(clone_name)
            sleep(1)
            driver.find_element_by_xpath("//button[@type='submit']").click()

            driver.find_element_by_xpath("//td[2]/a/i").click()
            # click plus sign to get the clone name
            sleep(1)
            tolog("Verify the clone name in clone list")
            validatelist.append(VerifyWords(driver, ({clone_name})))
            sleep(1)

            # click volume to show latest clone for the volume
            tolog("Verify the latest clone name in volume page")
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("//a/small").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, ({clone_name})))

            tolog("Modify clone name")
            driver.find_element_by_xpath("//div[2]/div/ul/li[3]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("//button[4]").click()
            sleep(1)
            driver.find_element_by_xpath("//td[2]/a/i").click()
            sleep(1)
            driver.find_element_by_xpath("//tr[3]/td[7]/pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_link_text("Modify Clone").click()
            driver.find_element_by_name("name").clear()
            modifiedname=random_key(10)
            driver.find_element_by_name("name").send_keys(modifiedname)
            sleep(1)
            driver.find_element_by_xpath("//div[3]/div/div/div/div[2]/button").click()
            sleep(1)
            driver.find_element_by_xpath("//td[2]/a/i").click()
            sleep(1)
            validatelist.append(VerifyWords(driver, ({modifiedname})))

            tolog("Export and Un-export clone")
            sleep(1)
            driver.find_element_by_link_text("Volume").click()
            sleep(1)
            driver.find_element_by_xpath("//pr-gear-button/div/a").click()
            sleep(1)
            driver.find_element_by_link_text("Snapshot & Clone").click()
            sleep(2)



            for i in range(3):
                sleep(1)
                driver.find_element_by_xpath("//td[2]/a/i").click()
                if driver.find_element_by_xpath("//tr[3]/td[3]").text == "Exported":

                    # driver.find_element_by_xpath("//div[2]/div/ul/li[3]/a/span").click()
                    # sleep(1)
                    # driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
                    # sleep(1)
                    # driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
                    # sleep(1)
                    # driver.find_element_by_xpath("//button[4]").click()
                    # sleep(1)
                    # driver.find_element_by_xpath("//td[2]/a/i").click()
                    sleep(1)
                    driver.find_element_by_xpath("//tr[3]/td[7]/pr-gear-button/div/a").click()
                    sleep(1)
                    # driver.find_element_by_link_text("Unexport Clone").click()

                    driver.find_element_by_link_text("Un-export Clone").click()
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Clone was un-exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Clone was un-exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

                    if driver.find_element_by_xpath("//tr[3]/td[3]").text == "Un-Exported":
                        tolog("Un-exported successfully.")
                else:

                    sleep(1)
                    driver.find_element_by_xpath("//tr[3]/td[7]/pr-gear-button/div/a").click()
                    sleep(1)
                    # driver.find_element_by_link_text("Unexport Clone").click()

                    driver.find_element_by_link_text("Export Clone").click()
                    sleep(1)
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Clone was exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Clone was exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

                    if driver.find_element_by_xpath("//tr[3]/td[3]").text == "Exported":
                        tolog("Exported successfully.")


        except:
            driver.get_screenshot_as_file("snapshot at " +
                                          re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                              time.time()))) + "create_delete_multi" + "." + "png")
            tolog("Error: please refer to the screen-shot in the folder")
            validatelist.append("True")
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
