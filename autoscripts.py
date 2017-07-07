# -*- coding: utf-8 -*-
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import sys
import testlink
import subprocess
import string
import datetime
import glob
from sgmllib import SGMLParser
from HTMLParser import HTMLParser
import importlib
#from Buzzer import verifyBuzzerInfo
# The initial version is from Nov 4, 2016
# get the basic ideas about the testlink API
# get basic info about the project, test plan, test suite, test case
# retrieve the test cases to be executed on specific platforms
# then execute the test cases on specific platforms
# update the test case result to testlink

def getduration(timestr):
    sec_min = 0
    timelist = list()
    timelist = string.split(timestr, ':')
    if int(timelist[2]) >= 30:
        sec_min = 1
    min = int(timelist[0]) * 60 + int(timelist[1]) + sec_min
    return min

def run_function(function):
    function()
    # verifyBuzzerInfo()



class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


if __name__ == "__main__":
    lname = "jacky"
    jacky = '2e99a3e8bb235adb1c0c06c7e17b13a2'
    zach="1e2a6e7af20e5c274174ff68e2ba63a2"
    hulda='a11277ff4b69a6152210e9923ab3796b'
    robot="31c13726fc2bae727aa02faaaa574892"
    if lname=="jacky":
        new_adminjl_key= jacky
    elif lname=="zach":
        new_adminjl_key = zach
    elif lname=="hulda":
        new_adminjl_key=hulda
    else:
        new_adminjl_key = robot
    # # new_testlink="http://192.168.252.175/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    #new_ip_testlink = "http://10.10.10.3/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    new_ip_testlink = "http://192.168.252.104/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    tls = testlink.TestlinkAPIClient(new_ip_testlink, new_adminjl_key)
    # test case notes
    Notes = 'testlink.notes'
    stepsnum=0
    NeedRun=False
    for project in tls.getProjects():
        if project['name'] == 'HyperionDS':
            testsuiteID= tls.getFirstLevelTestSuitesForTestProject(project['id'])[-1]['id']
            hastestsuite=False
            testsuite=tls.getTestCasesForTestSuite(testsuiteID,True,'full')
            for testplan in tls.getProjectTestPlans(1426):
                if testplan["active"]=="1" and "gui" in testplan["name"]:
                    tcdict = tls.getTestCasesForTestPlan(testplan['id'])
                    if type(tcdict) == dict:
                        tcdict_x = sorted(tcdict.items())
                        for eachtestcase in tcdict_x:
                            testcaseid=eachtestcase[0]
                            for key in eachtestcase[1]:
                                if key!='13':
                                    continue
                                else:
                                    TC_Platform = eachtestcase[1]['13']
                                    Platform_Name = TC_Platform['platform_name']
                                    TC_Name = TC_Platform['tcase_name']
                                    TC_execution = TC_Platform['exec_status']
                                    tcsteps = tls.getTestCase(TC_Platform['tcase_id'])[0]['steps']
                                    steps = [{'step_number': '1',
                                              'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> array -a add -p 1,2,3 -l "ID=2,alias=L0,raid=5,capacity=10gb,stripe=512kb,sector=4kb,writepolicy=writeback,readpolicy=nocache,parity=left"\r\nWarning: ld no. 1 - exceeds max sector size, adjust to 512 Bytes\r\nError (0x4021): Physical drive in use\r\n \r\nadministrator@cli> ',
                                              'result': 'p'}, {'step_number': '2',
                                                               'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> logdrv -v\r\n \r\n-------------------------------------------------------------------------------\r\nLdId: 0                                LdType: HDD\r\nArrayId: 0                             SYNCed: Yes\r\nOperationalStatus: OK\r\nAlias: \r\nSerialNo: 495345200000000000000000E27BAA63DF120006\r\nWWN: 22bc-0001-5556-12f2               PreferredCtrlId: 1\r\nRAIDLevel: RAID5                       StripeSize: 64 KB\r\nCapacity: 2 GB                         PhysicalCapacity: 3 GB\r\nReadPolicy: NoCache                    WritePolicy: WriteThru\r\nCurrentWritePolicy: WriteThru\r\nNumOfUsedPD: 3                         NumOfAxles: 1\r\nSectorSize: 512 Bytes                  RAID5&6Algorithm: right asymmetric (4)\r\nTolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A\r\nRaid6Scheme: N/A\r\nHostAccessibility: Normal\r\nALUAAccessStateForCtrl1: Active/optimized\r\nALUAAccessStateForCtrl2: Standby\r\nAssociationState: no association on this logical drive\r\nStorageServiceStatus: no storage service running\r\nPerfectRebuild: Disabled\r\n \r\nadministrator@cli> ',
                                                               'result': 'p'}]
                                    TC_Result_Steps = list()
                                    stepnote = list()
                                buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                buildname = buildnamelist[-1]['name']
                                testplanexec = tls.getTestCasesForTestPlan(testplan['id'])
                                exec_onbuild = testplanexec[TC_Platform['tcase_id']]['13']['exec_on_build']
                                if buildnamelist[-1]['id'] > exec_onbuild or TC_execution == 'f':
                                    NeedRun=True
                                # added this part on April 15th, 2017
                                # for build acceptance testing
                                # new build will be created through the following line
                                # buildnumber
                                    #                                   'Notes for the Build',
                                    #                                   releasedate="2016-12-31")
                                if NeedRun or TC_Name=="build_verification":# or TC_execution != 'f':
                                        #one test case only contains one step, is that function.
                                        # 2016.12.29
                                        # to determine testcases's testsuite id
                                        # print testsuite
                                        for each in testsuite:
                                            if each['id']==testcaseid:
                                                testsuitename=each['tsuite_name']
                                                hastestsuite=True
                                                # added on April 25th, 2017
                                                # to execute test cases by assigned user
                                        loginname=tls.getTestCaseAssignedTester(testplan['id'], eachtestcase[1]['13']['full_external_id'], buildname=buildname,platformname=Platform_Name)
                                        if hastestsuite and (lname==loginname[0]['login'] or lname=="robot"):
                                            print "The test cases under " + testplan['name'] + " of " + project[
                                                'name'] + " are as following:\n"
                                            start = time.time()
                                            stepsnum=len(tcsteps)
                                            for i in range(stepsnum):
                                                open(Notes, 'w').close()
                                                step_Result = 'n'
                                                stepstr = (string.replace(
                                                    string.replace(string.replace(tcsteps[i]['actions'], '<p>\n\t', ''), '</p>', ''),
                                                    '&quot;', '"')).replace("\n","")
                                                print stepstr
                                                os.system("python " + stepstr + '.py')
                                                fp= open(Notes,'r')
                                                note=fp.read()
                                                fp.close()
                                                # determine the execution result that will be updated to testlink.
                                                while "'result':" in note:
                                                    if "'result': 'f'" in note:
                                                        step_Result = 'f'
                                                        note = string.replace(note, "'result': 'f'",'')
                                                    else:
                                                        step_Result = 'p'
                                                        note = string.replace(note, "'result': 'p'", '')
                                                TC_Result_Steps.append(
                                                    {'step_number': str(i+1), 'result': step_Result, 'notes': note})
                                            for each in TC_Result_Steps:
                                                if each['result']!='p':
                                                    TC_Result='f'
                                                    break
                                                else:
                                                    TC_Result='p'
                                            # update test result remotely using API
                                            Update_timestamp = (
                                                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                                            # duration_min = getduration(str(TC_execution_duration))
                                            elasped = time.time() - start
                                            duration_min=str(elasped/60)
                                            buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                            buildname = buildnamelist[-1]['name']
                                            #TC_Result_Steps=[{'step_number': '0', 'notes': 'step1', 'result': 'f'}, {'step_number': '1', 'notes': 'step2 ', 'result': 'p'}]
                                            getExecution = tls.reportTCResult(TC_Platform['tcase_id'], testplan['id'],
                                                                              buildname, TC_Result,
                                                                              'automated test cases', guess=True,
                                                                              testcaseexternalid=TC_Platform['external_id'],
                                                                              platformname=TC_Platform['platform_name'],
                                                                              execduration=duration_min,
                                                                              timestamp=Update_timestamp,
                                                                              steps=TC_Result_Steps)
                                            print TC_Name + " on " + Platform_Name + " under " + testplan['name'] + " of " + project['name'] +" has been updated to testlink."
                                                    #  upload screenshot attachments if there's any mistake during the execution.
                                            #ExecutionID=getExecution[0]['id']
                                            #pngfiles = glob.glob(r'D:\\Hyperion-ds-script\\GUI\\pictu\\*.png')
                                            # if TC_Result == 'f':
                                            #     for png in pngfiles:
                                            #         tls.uploadExecutionAttachment(png, ExecutionID, 'reference screenshot',
                                            #                                       'reference screenshot')
                                            #         print 'The ' + png + ' has been uploaded to testlink.'
                                            #         os.remove(png)