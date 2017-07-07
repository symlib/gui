# -*- coding:utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
import re
#This test is use Firefox browser

def loginFirefox():
    #fp = webdriver.FirefoxProfile("C:/Users/hulda/AppData/Roaming/Mozilla/Firefox/Profiles/d8ot5jng.firefox")
    #fp.accept_untrusted_certs = True
    #driver = webdriver.Firefox(firefox_profile=fp)
    driver = webdriver.Firefox()
    subsys_url = "https://10.84.2.164"
    driver.implicitly_wait(30)
    driver.get(subsys_url)
    sleep(0.5)
    driver.find_element_by_name('username').clear()
    sleep(0.5)
    driver.find_element_by_name('username').send_keys('administrator')
    driver.find_element_by_name('password').clear()
    sleep(0.5)
    driver.find_element_by_name('password').send_keys('password')
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="frame"]/div/div[2]/form/div[4]/button').click()
    sleep(2)
    return driver

def loginIE():
    driver = webdriver.Ie("c:\Python27\IEDriverServer.exe")
    subsys_url = "https://10.84.2.116"
    driver.implicitly_wait(30)
    driver.get(subsys_url)
    sleep(2)
    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys('administrator')
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys('password')
    driver.find_element_by_xpath('//*[@id="frame"]/div/div[2]/form/div[4]/button').click()
    sleep(6)
    return driver


if __name__ == "__main__":
    loginFirefox()











