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
        sleep(1)

        validatelist = list()
        try:

            driver.find_element_by_xpath("//div[2]/div/ul/li[4]/a/span").click()
            sleep(1)
            driver.find_element_by_xpath("//div/ul/li[2]/a/span/span").click()
            sleep(1)
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            sleep(1)
            # firstly, check if there are 6 clones included.
            if driver.find_element_by_xpath("//tr[2]/td[2]/small").text=="(6 Clones included)":
                tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)



                tolog("Delete clone from gear button")


                driver.find_element_by_xpath("//td[2]/a/i").click()
                sleep(1)
                driver.find_element_by_xpath("//tr[3]/td[7]/pr-gear-button/div/a").click()
                sleep(1)
                driver.find_element_by_xpath("//tr[3]/td[7]/pr-gear-button/div/ul/li[3]/a").click()
                sleep(1)
                driver.find_element_by_name("name").clear()
                driver.find_element_by_name("name").send_keys("confirm")
                sleep(1)
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
                sleep(1)
                if driver.find_element_by_xpath("//tr[2]/td[2]/small").text=="(5 Clones included)":
                    #tolog("One clone is deleted successfully.")
                    tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)

                    tolog("Delete clone from selection")
                    sleep(1)
                    driver.find_element_by_xpath("//tr[2]/td[2]/a/i").click()
                    sleep(1)
                    driver.find_element_by_xpath("//tr[3]/td[1]/input").click()
                    sleep(1)
                    driver.find_element_by_xpath("//div/div/div/button[4]").click()
                    sleep(1)

                    driver.find_element_by_name("name").clear()
                    driver.find_element_by_name("name").send_keys("confirm")
                    sleep(1)
                    driver.find_element_by_xpath("//button[@type='submit']").click()
                    sleep(2)

                    driver.find_element_by_xpath("html/body/div[1]/div/div/div[3]/button").click()
                    sleep(2)
                    #tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)
                    if driver.find_element_by_xpath("//tr[2]/td[2]/small").text == "(4 Clones included)":
                        tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)
                        tolog("Delete clones from multi-selection")
                        driver.find_element_by_xpath("//tr[2]/td[2]/a/i").click()
                        sleep(1)
                        driver.find_element_by_xpath("//tr[3]/td[1]/input").click()
                        sleep(1)
                        driver.find_element_by_xpath("//tr[4]/td[1]/input").click()
                        sleep(1)
                        driver.find_element_by_xpath("//div/div/div/button[4]").click()
                        sleep(1)

                        driver.find_element_by_name("name").clear()
                        driver.find_element_by_name("name").send_keys("confirm")
                        driver.find_element_by_xpath("//button[@type='submit']").click()
                        sleep(2)

                        driver.find_element_by_xpath("html/body/div[1]/div/div/div[3]/button").click()
                        sleep(3)
                        #tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)
                        if driver.find_element_by_xpath("//tr[2]/td[2]/small").text == "(2 Clones included)":
                            tolog(driver.find_element_by_xpath("//tr[2]/td[2]/small").text)

                            tolog("Delete clones from delete all clones")
                            sleep(1)
                            driver.find_element_by_xpath("//tr[2]/td[2]/a/i").click()
                            sleep(1)
                            driver.find_element_by_xpath("//tr[1]/th[1]/input").click()

                            sleep(1)
                            driver.find_element_by_xpath("//div/div/div/button[4]").click()
                            sleep(1)

                            driver.find_element_by_name("name").clear()
                            driver.find_element_by_name("name").send_keys("confirm")
                            sleep(1)
                            driver.find_element_by_xpath("//button[@type='submit']").click()
                            sleep(2)

                            driver.find_element_by_xpath("html/body/div[1]/div/div/div[3]/button").click()
                            # sleep(3)
                            if not self.is_element_present(By.XPATH,"//tr[2]/td[2]/small"):

                                tolog("All Clones are deleted.")

            else:
                Failflag = True
                tolog("There're no "+driver.find_element_by_xpath("//tr[2]/td[2]/small").text)

        except:
            Failflag = True
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
