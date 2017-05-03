# -*- coding: utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import sys
from to_log import tolog


def VerifyWords(driver, wordlist):
    ValidationError=False
    # time.sleep(1)
    for each in wordlist:
        time.sleep(0.5)
        if re.search(each, driver.find_element_by_css_selector("BODY").text):
            tolog(each +' is verified.')
        else:
            tolog(each + ' is not verified.')
            ValidationError = True
            break
    return ValidationError

