
from selenium import webdriver
from Helpers import RadiobuttonHelper
from Helpers.RadiobuttonHelper import RadioButtonHelper
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from Helpers.LoginPage import LoginPage
from Helpers.Base import Base
from Helpers.createProjectSolaraUI import createProjectEast
from Helpers.PlanCreationHelper import planPageSolaraUI
from Helpers.NewInputHelper import CreateCollections
import time,os
import pandas as pd
import csv
from utilities.reportScreenshot import add_screenshot
import pytest
import random,string
from selenium.webdriver.common.keys import Keys 
from utilities.logScreenshot import cLogScreenshot
import string
import random
from Helpers.ExcelAutomationHelper import ExcelAutomationHelper
from Helpers.Design_ComputeHelper import AD_DesignPageHelperfunctions

class Test_EndtoEnd_TwoArmCont:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArmContinuous_UIvalidation")
    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()

    @pytest.fixture(params=TCList)
    def testcase(self,request):
        return request.param

    @pytest.mark.EndtoEnd
    def test_EndtoEnd_TwoArmCont(self,testcase,setup,extra,request):
        
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} started")
        # read the testcase test data file path from wrapper testdata excel file
        path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
        # read the testcase title from wrapper testdata excel file
        title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
        '''
        Read Testdata file and run through the application iteration-wise
        '''
        datafile = pd.read_excel( path, sheet_name = "Testdata" )
        dataFile1= pd.read_excel( path, sheet_name = "Superiority" )
        dataFile2= pd.read_excel( path, sheet_name = "Super Superiority" )

        self.driver = setup
        self.driver.get(self.baseURL)
        # instantiate logscreenshot class
        LogScreenshot = cLogScreenshot(self.driver,extra)
        # Instantiate the Base 
        self.base = Base(self.driver)
        # instantiate the logger class
        logger = LogGen.loggen()

        # initiate the test case status list
        tc_status = []
        # for i in range(len(Testcaselist)):
        self.loginpage = LoginPage(self.driver,extra)
        self.createProjectSolara = createProjectEast(self.driver,extra)
        self.DesignHelper = AD_DesignPageHelperfunctions(self.driver,extra)
        self.createCollection = CreateCollections(self.driver,extra)
        self.functionsforexcel = ExcelAutomationHelper(self.driver, extra)
        self.radio_button_helper = RadioButtonHelper(self.driver,extra)          
        xls=pd.ExcelFile(path)
        sheetname=xls.sheet_names
        print(sheetname)

        time.sleep(3)                  
        for tc_index in range(len(self.TCList)):
            print(self.TCList)
            try:
                self.loginpage.complete_login(self.username, self.password, tc_index)
                self.createProjectSolara.projectCreation()
                time.sleep(10)
                self.plainPagesolaraui.NewplanCreation("Two Arm","Continuous")
                # self.execute_test_iteration(dataFile, tc_index, extra)
            except Exception as e:
                LogScreenshot.fLogScreenshot( message = f"Error in test case {self.TCList[tc_index]}: {e}, Unable to create plan",
                        pass_ = False, log = True, screenshot = True)
                break

            for i in range(len(datafile)):
                try:
                    self.createCollection.createNewInputSet(i) 
                    self.base.click("GenerateDesign",UnivWaitFor=15)
                    LogScreenshot.fLogScreenshot( message = f"Clicked on 'Generative Design' option and landed in Design page",
                            pass_ = True, log = True, screenshot = True)
                    time.sleep(10)
                    self.base.selectByvisibleText("InputMethod", 'Individual Means', UnivWaitFor=5)
                    LogScreenshot.fLogScreenshot( message = f"Selected Individual Means option from the InputMethod dropdown",
                            pass_ = True, log = True, screenshot = True)                
                        
                    # Select the test statistic option
                    self.base.selectByvisibleText("TestStatisticDD", 'Z', UnivWaitFor=5)
                    LogScreenshot.fLogScreenshot( message = f"Selected Z option from the dropdown",
                                                pass_ = True, log = True, screenshot = True)
                    
                    self.base.selectByvisibleText("InputMethod", 'Individual Means', UnivWaitFor=5)
                    LogScreenshot.fLogScreenshot( message = f"Selected Individual Means option from the InputMethod dropdown",
                            pass_ = True, log = True, screenshot = True)   
                except Exception as e:
                    LogScreenshot.fLogScreenshot( message = f"Error in creating inputset and selecting dropdowns : {e}",
                        pass_ = False, log = True, screenshot = True)   
                    tc_status.append("FAIL")                 
                try:
                    HypotesisDrpdown=datafile.loc[i,'DesignType']
                    self.base.selectByvisibleText("HypothesisDD",HypotesisDrpdown,UnivWaitFor = 10)
                    self.base.getdefaultselectedValueFromDropdown("HypothesisDD")
                    LogScreenshot.fLogScreenshot( message = f"Selected the option Hypothesis from Dropdown ",
                        pass_ = True, log = True, screenshot = True)
                except Exception as e:
                    LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                        pass_ = False, log = True, screenshot = True)                     
                
                self.DesignHelper.SelectAssurance_DistributionDropdown("User Specified",UnivWaitFor=2)
                LogScreenshot.fLogScreenshot( message = f"Verified the functionality of User Specified",
                        pass_ = False, log = True, screenshot = True) 
                                  
                self.base.click("SampleDesignRB", UnivWaitFor=5)
                if self.base.getAttribute("SampleSizeTB",'value') == 'Computed':
                        print(f"Text box SampleSize Textbox is disabled with the text 'Computed'")
                        LogScreenshot.fLogScreenshot( message = f"Sample Size Radio button clicked and Sample Size textbox is disabled with the text 'Computed' ",
                        pass_ = True, log = True, screenshot = True) 
                else:
                        print(f"Text box SampleSize Textbox is not disabled with the text 'Computed'")

                self.base.click("Type1ErrorRB", UnivWaitFor=5)
                if self.base.getAttribute("Type1ErrorTB",'value') == 'Computed':
                        print(f"Text box Type1Error Textbox is disabled with the text 'Computed'")
                        LogScreenshot.fLogScreenshot( message = f"Type1Error TB Radio button clicked and Type1Error textbox is disabled with the text 'Computed' ",
                        pass_ = True, log = True, screenshot = True) 
                else:
                        print(f"Text box Type1Error Textbox is not disabled with the text 'Computed'")

                self.base.click("PowerRB", UnivWaitFor=5)
                if self.base.getAttribute("PowerTB",'value') == 'Computed':
                        print(f"Text box Power Textbox is disabled with the text 'Computed'")
                        LogScreenshot.fLogScreenshot( message = f"Power Radio button clicked and Power textbox is disabled with the text 'Computed' ",
                        pass_ = True, log = True, screenshot = True) 
                else:
                        print(f"Text box Power Textbox is not disabled with the text 'Computed'")

                self.base.click("DifferenceofMeansRB", UnivWaitFor=5)
                if self.base.getAttribute("DifferenceofMeansTB",'value') == 'Computed':
                        print(f"Text box DifferenceofMeans Textbox is disabled with the text 'Computed'")
                        LogScreenshot.fLogScreenshot( message = f"DifferenceofMeans Radio button clicked and DifferenceofMeans textbox is disabled with the text 'Computed' ",
                        pass_ = True, log = True, screenshot = True) 
                else:
                        print(f"Text box DifferenceofMeans Textbox is not disabled with the text 'Computed'")

                self.base.click("SampleDesignRB", UnivWaitFor=5)
                LogScreenshot.fLogScreenshot( message = f"Clicked on  Radio button Sample Design",
                        pass_ = True, log = True, screenshot = True) 

                try:     
                    self.DesignHelper.ToggleAssurance_POS("TestStatisticDD","Z",UnivWaitFor=10)
                    try:
                        is_element_verified = self.DesignHelper.verify_elements_WithAccural()
                        if is_element_verified:
                            print("Element is verified successfully!")
                        else:
                            print("Element verification failed.")
                    except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in verifying the element {e}",
                        pass_ = False, log = True, screenshot = True)
                except Exception as e:
                    LogScreenshot.fLogScreenshot( message = f"Error in verifying the element {e}",
                        pass_ = False, log = True, screenshot = True)
                    tc_status.append("FAIL")
                try:
                    # Verify dropdown options for 'with Accural'
                    DistributionMethodList= ['Select ...','Normal', 'Uniform', 'User Specified']
                    # Assur_InputmethodList= ['Select ...','E(δ) and SD(δ) ', 'Percentiles of δ', 'Percentiles of δ/σ']
                    Assur_InputmethodList = ['Select ...', 'E(\u03B4) and SD(\u03B4)', 'Percentiles of \u03B4', 'Percentiles of \u03B4/σ']
                    TestTypeList=['Select ...','1-Sided','2-Sided','2-Sided (Asymmetric)']
            
                    self.DesignHelper.compare_dropdown_options( "DistributionMethodDD", DistributionMethodList)
                    print("expected items of Distribution dropdown"- DistributionMethodList)
                    LogScreenshot.fLogScreenshot( message = f"Distribution Dropdown items are verified",
                         pass_ = True, log = True, screenshot = True) 
                    
                    self.DesignHelper.compare_dropdown_options( "Assur_InputmethodDD", Assur_InputmethodList)
                    print("expected items of Assurance dropdown"- Assur_InputmethodList)
                    LogScreenshot.fLogScreenshot( message = f"Assurance Input Method Dropdown items are verified",
                         pass_ = True, log = True, screenshot = True) 

                    self.DesignHelper.compare_dropdown_options( "TestTypeDD", TestTypeList)
                    print("expected items of Assurance dropdown"- Assur_InputmethodList)
                    LogScreenshot.fLogScreenshot( message = f"Assurance Input Method Dropdown items are verified",
                         pass_ = True, log = True, screenshot = True)

                except Exception as e:
                     LogScreenshot.fLogScreenshot( message = f"Error in verifying the Dropdown items {e}",
                         pass_ = False, log = True, screenshot = True) 

                # Enable Enrollment page
                # try:
                #     self.base.click("Enrollment_leftpanellink",UnivWaitFor = 5)
                #     self.base.click("EnrollmentToggle", UnivWaitFor=10)
                #     LogScreenshot.fLogScreenshot( message = f"Clicked On Enrollment Link and toggled",
                #         pass_ = True, log = True, screenshot = True)
                    
                # except Exception as e:
                #     LogScreenshot.fLogScreenshot( message = f"Error in Navigating to the Page Enrollment {e}",
                #         pass_ = False, log = True, screenshot = True)
                # self.base.click("InputSetBackbutton", UnivWaitFor=5)
                # LogScreenshot.fLogScreenshot( message = f"Clicked On Input set back button",
                #         pass_ = True, log = True, screenshot = True)

        tc_status.append("PASS")
        self.base.switchout()
            # logout and return to login page
            # self.loginpage.logout() 

        #Close the current browser window
        self.driver.quit()
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} completed")

        if "FAIL" in tc_status:
            assert False
            # raise enter message here
        else:
            assert True

