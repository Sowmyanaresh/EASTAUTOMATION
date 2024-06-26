from argparse import Action
from cgitb import text
from concurrent.futures import thread
from email.policy import default
from gettext import find
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from Helpers.LoginPage import LoginPage
from Helpers.VisualsPage import VisualsPage
from Helpers.openTOA import cOpenTOA
from Helpers.Base import Base
from Helpers.apiProjectGen.createProject import cCreateProject
import pandas as pd
from utilities.reportScreenshot import add_screenshot
from pytest_html import extras
import pytest
import random,string
from selenium.webdriver.common.keys import Keys 
from utilities.logScreenshot import cLogScreenshot
from Helpers.weightsPage import cWeightsPage
from Helpers.filtersPage import cFiltersPage
from Helpers.tablePage import cTablePage
import ast,time
from utilities.downloadHandler import cDownloadHandler
from selenium.webdriver.common.by import By
import csv
import os
from selenium.common.exceptions import NoSuchElementException



class Test_003_TOA:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD( "login" )

    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()

    @pytest.fixture(params=TCList)
    def testcase(self,request):
        return request.param

    @pytest.mark.c2
    def test_logoutCheck(self,testcase,setup,extra,request):
        LogGen.loggen().info(f"test_logoutCheck - {testcase} started")
        # read the testcase test data file path from wrapper testdata excel file
        path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
        # read the testcase title from wrapper testdata excel file
        title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
        dataFile = pd.read_excel( path, sheet_name = "datafile" )
        
        # storing values from the data file to enter in the report
        request.node._filepath = path
        request.node._title = title
        request.node._tcid = testcase
        request.node._name = "LoginCheck"

        self.driver = setup
        self.driver.get(self.baseURL)

        # instantiate logscreenshot class
        LogScreenshot = cLogScreenshot(self.driver,extra)

        # Instantiate the Base class
        self.base = Base(self.driver)
        
        # initiate the test case status list
        tc_status = []
        for i in range(len(dataFile)):
            # Complete the login process. If login fails, log out and return to login page
            self.loginpage = LoginPage(self.driver,extra)
            try:
                self.loginpage.complete_login(self.username,self.password,i)
                LogScreenshot.fLogScreenshot( message = f"Login Successful",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
                tc_status.append("FAIL")
                break
            tc_status.append("PASS")
        self.base.switchout()
        # logout and return to login page
        self.loginpage.logout()
        tc_status.append("PASS")

        LogGen.loggen().info(f"test_smoke - {testcase} completed")

        if "FAIL" in tc_status:
            assert False
            # raise enter message here
        else:
            assert True