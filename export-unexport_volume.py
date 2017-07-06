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

class ExportUnexportVolume(unittest.TestCase):


    def test_ExportUnexport_volume(self):
        Failflag = False
        self.driver = loginFirefox()
        # self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver



        tolog("Start to Export/Unexport volume")
        # driver.find_element_by_link_text("Pool").click()
        # driver.find_element_by_xpath("//div[2]/button").click()
        # sleep(1)
        #
        # poolnum0=poolnum1=volnum0=volnum1=snapnum0=snapnum1=clonenum0=clonenum1=0
        validatelist = list()
        sleep(2)
        try:
            # export/unexport from volume list page
            # 2017-07-06

            for j in range (2):
                tolog("Export/unexport from volume list page")
                status = False  # exported
                sleep(5)
                # driver.find_element_by_link_text("Pool").click()
                # sleep(1)
                # driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
                # sleep(2)
                driver.find_element_by_link_text("Volume").click()
                sleep(2)
                if re.search("Un-Exported", driver.find_element_by_css_selector("BODY").text):
                    status=True
                if status: #not un-exported, Exported
                    # the status is Un-exported
                    #validatelist.append(VerifyWords(driver, ("Exported")))
                    sleep(2)
                    driver.find_element_by_xpath("//li/ul/li/a/span/span").click()
                    sleep(2)
                    driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
                    sleep(2)
                    driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
                    sleep(1)
                    #validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was exported successfully." );
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

                else:
                    #validatelist.append(VerifyWords(driver, ("Exported")))
                    sleep(2)
                    driver.find_element_by_xpath("//li/ul/li/a/span/span").click()
                    sleep(2)
                    driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
                    sleep(2)
                    driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
                    sleep(1)
                    validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was un-exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was un-exported successfully." );
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")



                # export/unexport from volume list page
                # 2017-07-06
                tolog("Export/unexport from volume  page")
                status = False
                driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
                sleep(5)
                if re.search("Un-Exported", driver.find_element_by_css_selector("BODY").text):
                    status=True
                if status: #
                    #validatelist.append(VerifyWords(driver, ("Un-Exported")))
                    sleep(1)
                    driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
                    sleep(1)
                    #validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was exported successfully." );
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")

                else:
                    #validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    sleep(1)
                    driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
                    sleep(1)
                    validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was un-exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was un-exported successfully." );
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")



                # export/unexport from volume list page
                # 2017-07-06
                tolog("Export/unexport from gear button page")
                status=False
                sleep(5)
                driver.find_element_by_xpath(".//*[@id='sidebar-menu']/ul/li[4]/a").click()
                sleep(1)
                driver.find_element_by_link_text("Volume").click()
                sleep(2)
                if re.search("Un-Exported", driver.find_element_by_css_selector("BODY").text):
                    status=True
                if status:
                    #sleep(1)
                    #validatelist.append(VerifyWords(driver, ("Un-Exported")))
                    sleep(6)
                    # driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                    # sleep(3)
                    driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                    sleep(1)
                    driver.find_element_by_link_text("Export").click()
                    sleep(1)

                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")
                else:
                    sleep(6)
                    # driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                    # sleep(3)
                    driver.find_element_by_xpath("//pr-gear-button/div/a").click()
                    sleep(1)
                    driver.find_element_by_link_text("Un-export").click()
                    sleep(2)
                    validatelist.append(VerifyWords(driver, ({"Un-Exported"})))
                    for i in range(60):
                        try:
                            if re.search(r"^[\s\S]*Volume was un-exported successfully.[\s\S]*$",
                                         driver.find_element_by_css_selector("BODY").text):
                                tolog("Volume was un-exported successfully.");
                                break
                        except:
                            pass
                        time.sleep(1)
                    else:
                        self.fail("time out")


        except:
            driver.get_screenshot_as_file("snapshot at " +
                                          re.sub(':', '.', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                              time.time()))) + "create_delete_multi" + "." + "png")
            tolog("Error: please refer to the screen-shot in the folder")
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
