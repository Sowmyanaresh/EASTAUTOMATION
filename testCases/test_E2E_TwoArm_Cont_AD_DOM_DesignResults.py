from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from Helpers.LoginPage import LoginPage
from Helpers.Base import Base
from Helpers.PlanCreationHelper import PlanCreationHelper
import time,os
import pandas as pd
from selenium.webdriver.common.by import By
from utilities.reportScreenshot import add_screenshot
import pytest
from selenium.webdriver.common.keys import Keys 
from utilities.logScreenshot import cLogScreenshot
from Helpers.ExcelHelper import Excel_HelperFunctions
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions


class Test_EndtoEnd_TwoArmCont_DOM_Ad_Results:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArm_ADResults_DOM")
    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()
    
    @pytest.fixture(params=TCList)
    def testcase(self,request):
        return request.param

    @pytest.mark.EndtoEnd
    def test_EndtoEnd_TwoArmCont_DOM_AD_Results(self,testcase,setup,extra,request):
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} started")
        # read the testcase test data file path from wrapper testdata excel file
        path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
        # read the testcase title from wrapper testdata excel file
        title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
        '''
        Read Testdata file and run through the application iteration-wise
        '''
        datafile = pd.read_excel( path, sheet_name = "Testdata")
        self.driver = setup
        self.driver.get(self.baseURL)
        # instantiate logscreenshot class
        LogScreenshot = cLogScreenshot(self.driver,extra)
        # Instantiate the Base class
        self.base = Base(self.driver)
        logger = LogGen.loggen()
        # initiate the test case status list
        tc_status = []

        # Initialize the LoginPage instance
        self.loginpage = LoginPage(self.driver,extra)
        self.ProjectandPlancreation = PlanCreationHelper(self.driver,extra)
        self.DesignHelper = AD_DesignPageHelperfunctions(self.driver,extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)       
        '''
        New Project > create new inputs in iteration > Enter fields from Test data file >         
        '''
        time.sleep(3)                  
        print(self.TCList)
        for tc_index in range(len(self.TCList)):
            # try:
            #     self.loginpage.complete_login(self.username, self.password, tc_index)
            #     print("login successful")
            #     self.base.click("FirstProject", UnivWaitFor=30)
            #     self.base.click("InputSection", UnivWaitFor=10)
            #     self.base.click("InputSet_link", UnivWaitFor=10)
            #     print("Clicked on InputSection successful")
            #     LogScreenshot.fLogScreenshot(message="Clicked on input set", pass_=True, log=True, screenshot=True)
            # except Exception as e:
            #     LogScreenshot.fLogScreenshot(message=f"Error in creating input and selecting dropdowns Input: {e}", pass_=False, log=True, screenshot=True)
            try:
                self.loginpage.complete_login(self.username, self.password,tc_index)
                print("Login succesful")
                time.sleep(10)
                StudyObjective = datafile.at[0, 'StudyObjective']
                EndpointType = datafile.at[0, 'EndpointType']
                TargetPopulation = datafile.at[0, 'TargetPopulation']
                ControlArm = datafile.at[0, 'ControlArm']
                TreatmentArm = datafile.at[0, 'TreatmentArm']
                EndpointName = datafile.at[0, 'EndpointName']
                BetterResponse = datafile.at[0, 'BetterResponse']
                FollowUpTime = datafile.at[0, 'FollowUpTime']  
                self.ProjectandPlancreation.new_project_and_plan_creation(StudyObjective,EndpointType,TargetPopulation,ControlArm,TreatmentArm,EndpointName,BetterResponse,FollowUpTime)
                LogScreenshot.fLogScreenshot( message = f"Created TwoArm Plan", pass_ = True, log = True, screenshot = True)
                print("Plan created succesfully") 
            except Exception as e:
                LogScreenshot.fLogScreenshot( message = f"Error in test case {self.TCList}: {e}, Unable to create plan",
                        pass_ = False, log = True, screenshot = True)
                '''
                This script is for Individual Means with the Combination of Assurance
                '''
                # for i in range(len(datafile)):
            for row_index, row_data in datafile.iterrows():
                try:                    
                    try:
                        
                        # Perform actions on the input page based on current row_data
                        self.DesignHelper.perform_input_actions(row_index,row_data, LogScreenshot)    
                        print("creating input and Selecting dropdowns  \n")                
                    except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in creating input and selecting dropdowns Input: {e}",
                            pass_ = False, log = True, screenshot = True)                         
                    try:
                        print( "indexnumber-", row_index)
                        # print( "indexrowdata-", row_data)
                        self.DesignHelper.process_input_row_DOM(row_data)    
                        print("input from testdata into Design page is completed  \n")
                    except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in feeding testdata : {e}",
                            pass_ = False, log = True, screenshot = True)      
                        tc_status.append("FAIL")      

                    try:            
                        self.base.click("Savebutton", UnivWaitFor=5)
                        LogScreenshot.fLogScreenshot(message="Clicked on Save button", pass_=True, log=True, screenshot=True)
                        self.base.click("SaveCompute", UnivWaitFor=5)
                        LogScreenshot.fLogScreenshot(message="Clicked on Save&Compute button", pass_=True, log=True, screenshot=True)
                        self.base.click("Compute", UnivWaitFor=10)
                        LogScreenshot.fLogScreenshot(message="Clicked on Compute button", pass_=True, log=True, screenshot=True)        
                        # self.base.click("ResultSet1", UnivWaitFor=5)     
                        self.base.click("ResultsPage",UnivWaitFor=15)
                        LogScreenshot.fLogScreenshot( message = f"Clicked on Results Page ",
                            pass_ = True, log = True, screenshot = True) 
                        xpath = f"//a[contains(text(),'Result - Input Set {row_index + 1}')]"
                        print("clicked on : ", xpath)
                        self.driver.find_element(By.XPATH, xpath).click()
                        time.sleep(5)
                        LogScreenshot.fLogScreenshot( message = f"Clicked on Results-1 inputset Page ",
                            pass_ = True, log = True, screenshot = True)
                    except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in Generating results : {e}",
                            pass_ = False, log = True, screenshot = True) 
                        tc_status.append("FAIL") 

                    try:
                        # Results Validation Logic
                        self.DesignHelper.validate_results_DOM(datafile, row_data, LogScreenshot, tc_status)
                    except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in Generating results : {e}",
                            pass_ = False, log = True, screenshot = True) 
                        tc_status.append("FAIL") 
                    # break
                    self.base.click("CloseResult", UnivWaitFor=8)
                    LogScreenshot.fLogScreenshot(message=f"Closed the Result Page ",
                                        pass_=True, log=True, screenshot=True)
                except Exception as e:
                    LogScreenshot.fLogScreenshot(message=f"Error in iteration {e}",
                                        pass_=False, log=True, screenshot=True)

                if row_index == len(datafile) - 1:
                    break

        tc_status.append("PASS")
        # self.base.switchout()
            # logout and return to login page
            # self.loginpage.logout() 

        #Close the current browser window
        self.driver.quit()
        LogGen.loggen().info(f"{testcase} completed")

        if "FAIL" in tc_status:
            assert False
            # raise enter message here
        else:
            assert True
