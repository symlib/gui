# -*- coding:utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from print_result import printSF
import re
#This test is use Firefox browser

def login():
    fp = webdriver.FirefoxProfile('C:/Users/hulda/AppData/Roaming/Mozilla/Firefox/Profiles/d8ot5jng.firefox')
    fp.accept_untrusted_certs = True
    driver = webdriver.Firefox(firefox_profile=fp)
    subsys_url = "https://10.84.2.98"
    driver.implicitly_wait(30)
    driver.get(subsys_url)
    sleep(4)
    driver.find_element_by_name('username').clear()
    sleep(1)
    driver.find_element_by_name('username').send_keys('administrator')
    driver.find_element_by_name('password').clear()
    sleep(1)
    driver.find_element_by_name('password').send_keys('password')
    sleep(1)
    driver.find_element_by_xpath('//*[@id="frame"]/div/div[2]/form/div[4]/button').click()
    sleep(3)
    return driver
'''
    for i in range(60):
        try:
            if re.search(r"^[\s\S]*Model :Pegasus[\s\S]*$",
                         driver.find_element_by_css_selector("BODY").text): printSF(
                "Login Successfully and Pegasus is found."); break
        except:
            pass
        sleep(1)
    else:
        print '====='

'''




if __name__ == "__main__":
    login()















