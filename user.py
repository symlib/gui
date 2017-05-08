# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from time import sleep
from namegenerator import random_key
from namegenerator import address_generator
import random
from to_log import tolog
from VerifyWords import VerifyWords

Pass="'result': 'p'"
Fail="'result': 'f'"

class userOps(unittest.TestCase):
    def setUp(self):
        #use firefox
        self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(30)
        self.base_url = "https://10.84.2.98/"
        capabilities = webdriver.DesiredCapabilities().FIREFOX
        self.verificationErrors = []
        self.accept_next_alert = True
        # use IE
        # self.driver = webdriver.Ie("c:\Python27\IEDriverServer.exe")
        #
        # self.base_url = "https://10.84.2.164/"

        # capabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER
        # capabilities['acceptSslCerts'] = True
        #
        # driver = webdriver.Ie(capabilities=capabilities)


    
    def test_ops(self):
        Failflag = False

        validatelist=list()
        driver = self.driver

        sleep(1)

        driver.get(self.base_url + "/index.html")
        sleep(1)

        #print driver.find_element_by_id("overridelink")

        sleep(1)
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("administrator")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("password")

        sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        sleep(1)
        tolog("Verify creating a new user.")
        driver.find_element_by_css_selector("li[name=\"user\"] > a > span.ng-binding.ng-scope").click()

        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        sleep(1)
        idname=random_key(10)
        fullname=random_key(15)
        driver.find_element_by_name("id").clear()
        driver.find_element_by_name("id").send_keys(idname)
        driver.find_element_by_name("fulllname").clear()
        driver.find_element_by_name("fulllname").send_keys(fullname)

        pwd=random_key(8)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(pwd)
        driver.find_element_by_name("retypepassword").clear()
        driver.find_element_by_name("retypepassword").send_keys(pwd)
        sleep(1)
        email=address_generator()

        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(email)


        driver.find_element_by_name("privilege").click()
        sleep(1)
        privilege = ["Super", "Power", "Maintenance", "View"]
        priv="View"

        Select(driver.find_element_by_name("privilege")).select_by_visible_text(priv)
        #driver.find_element_by_css_selector("option[value=\"string:" + priv + "\"]").click()
        sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        for i in range(100):
            try:
                if re.search(r"^[\s\S]*New User was created successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("User %s was added successfully." % idname);

                    break
            except:
                pass
            sleep(0.1)
        else:
            Failflag = True
            self.fail("time out")
        sleep(1)
        validatelist.append(VerifyWords(driver,(idname,fullname,priv,email)))

        tolog("Verify modifying a user's settings.")
        # modify user settings
        sleep(1)
        driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        sleep(1)
        updatedfullname = "updated_" + fullname
        driver.find_element_by_name("displayname").clear()
        sleep(1)
        driver.find_element_by_name("displayname").send_keys(updatedfullname)
        sleep(1)
        updatedemail="updated_"+email
        driver.find_element_by_name("email").clear()
        sleep(1)
        driver.find_element_by_name("email").send_keys(updatedemail)
        sleep(1)
        privilege.remove(priv)

        updatedpriv=random.choice(privilege)
        # print ("the updatedpriv is %s" % updatedpriv)
        sleep(1)
        Select(driver.find_element_by_name("privilege")).select_by_visible_text(updatedpriv)
        sleep(1)
        # driver.find_element_by_css_selector("option[value=\"string:"+updatedpriv+"\"]").click()
        # sleep(1)
        Select(driver.find_element_by_name("privilege")).select_by_visible_text(updatedpriv)
        sleep(1)
        Select(driver.find_element_by_name("privilege")).select_by_visible_text(updatedpriv)
        Select(driver.find_element_by_name("privilege")).select_by_visible_text(updatedpriv)
        sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)
        for i in range(100):
            try:
                if re.search(r"^[\s\S]*User Settings were saved successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("User settings %s %s %s were saved successfully." % (updatedfullname,updatedemail,updatedpriv));

                    break
            except:
                pass
            sleep(0.1)
        else:
            Failflag = True
            self.fail("time out")
        time.sleep(2)
        validatelist.append(VerifyWords(driver, (updatedfullname, updatedemail, updatedpriv)))

        # change password
        tolog("Verify changing a new user's password.")
        driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        sleep(1)
        driver.find_element_by_xpath("//button[@type='button']").click()
        sleep(1)
        driver.find_element_by_name("newpwd").clear()
        driver.find_element_by_name("newpwd").send_keys("password")
        driver.find_element_by_name("newpwd").clear()
        sleep(1)
        driver.find_element_by_name("newpwd").send_keys("1")
        driver.find_element_by_name("retypepwd").clear()
        driver.find_element_by_name("retypepwd").send_keys("1")
        sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)
        for i in range(100):
            try:
                if re.search(r"^[\s\S]*User Password was changed successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("User Password was changed successfully." );

                    break
            except:
                pass
            sleep(0.1)
        else:
            Failflag = True
            self.fail("time out")

        tolog("Verify deleting the created user.")
        driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        sleep(1)
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("confirm")
        sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)
        for i in range(100):
            try:
                if re.search(r"^[\s\S]*User was deleted successfully.[\s\S]*$",
                             driver.find_element_by_css_selector("BODY").text):
                    tolog("User %s was deleted successfully."%idname);

                    break
            except:
                pass
            sleep(0.1)
        else:
            Failflag = True
            self.fail("time out")

        for val in validatelist:
            if val:
                Failflag = True
                break

        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)



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
