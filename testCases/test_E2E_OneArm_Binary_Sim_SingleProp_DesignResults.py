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
from Helpers.Sim_Result_Helper import Sim_Result_Helperfunctions
from Helpers.Sim_Design_Helper import Sim_DesignPageHelperfunctions
from Helpers.Sim_Enrollment_Helper import Sim_EnrollmentPageHelperFunctions
from Helpers.Sim_Response_Helper import Sim_ResponsePageHelperFunctions
from Helpers.Sim_SimulationSetup import Sim_SimulationSetupPageHelperFunctions


class Test_EndtoEnd_OneArmBinary_SP_Sim_Results:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArm_Continuous_SimResults_SingleProp")
    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()
    
    @pytest.fixture(params=TCList)
    def testcase(self,request):
        return request.param

    @pytest.mark.EndtoEnd
    def test_EndtoEnd_OneArmBinary_SP_Sim_Results(self,testcase,setup,extra,request):
        LogGen.loggen().info(f" {testcase} started")
        # read the testcase test data file path from wrapper testdata excel file
        path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
        # read the testcase title from wrapper testdata excel file
        title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
        '''
        Read Testdata file and run through the application iteration-wise
        '''
        datafile = pd.read_excel( path, sheet_name = "Testdata", keep_default_na=False)
        # dataFile1= pd.read_excel( path, sheet_name = "Teststastic-t" )
        # dataFile2= pd.read_excel( path, sheet_name = "Teststastic-z" )

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
        self.SimulationDesignHelper = Sim_DesignPageHelperfunctions(self.driver,extra)
        self.SimulationResponseHelperclass=Sim_ResponsePageHelperFunctions(self.driver, extra)
        self.SimulationEnrollmentHelperclass=Sim_EnrollmentPageHelperFunctions(self.driver, extra)    
        self.SimulationSetupHelperclass=Sim_SimulationSetupPageHelperFunctions(self.driver, extra)  
        self.SimresultHelper=Sim_Result_Helperfunctions(self.driver, extra)      
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
                time.sleep(6)
                self.base.click("FirstProject", UnivWaitFor=20)
            except Exception as e:
                LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
                tc_status.append("FAIL")

            for row_index, row_data in datafile.iterrows():
                                   
                self.base.click("ResultsPage",UnivWaitFor=10)
                LogScreenshot.fLogScreenshot( message = f"Clicked on Results page",
                        pass_ = True, log = True, screenshot = True)
                # self.base.click("ResultSet1", UnivWaitFor=3)
                self.base.click("Simulatebutton",UnivWaitFor=10)
                self.base.click("CreateInputSetbutton", UnivWaitFor=5)
                
                # Verify Analytical Design Page
                self.base.click("DesignPage", UnivWaitFor=5)

                # self.SimulationDesignHelper.Select_RandomizedMethod("Fixed Allocation", UnivWaitFor=2)
                # self.SimulationDesignHelper.Select_teststatistic('t','Unequal', UnivWaitFor=2)
                LogScreenshot.fLogScreenshot( message = f"Navigated to Designs ",
                        pass_ = True, log = True, screenshot = True)
                self.SimulationDesignHelper.process_Sim_input_row_SingleProportion_Design(row_data)
                LogScreenshot.fLogScreenshot( message = f"Entered all the fields in Designs page",
                        pass_ = True, log = True, screenshot = True)
    
                self.base.click("ResponsePage", UnivWaitFor=5)
                LogScreenshot.fLogScreenshot( message = f"Navigated to Response ",
                        pass_ = True, log = True, screenshot = True)
                self.SimulationResponseHelperclass.process_Sim_input_row_Response_SingleProportion(row_data)
                LogScreenshot.fLogScreenshot( message = f"Entered all the fields in Response page",
                        pass_ = True, log = True, screenshot = True)
                # self.SimulationResponseHelperclass.process_Sim_input_row_Response(row_data)
                
                self.base.click("EnrollmentPage", UnivWaitFor=4)
                LogScreenshot.fLogScreenshot( message = f"Navigated to Enrollment",
                        pass_ = True, log = True, screenshot = True)
                self.SimulationEnrollmentHelperclass.process_input_row_Sim_enrollement(row_data)
                # self.base.clickMultipleTimesOnElement("Addbutton", 1)
                LogScreenshot.fLogScreenshot( message = f"Entered all the fields in Enrollment page",
                        pass_ = True, log = True, screenshot = True)

                self.base.click("SimulationSetuplink", UnivWaitFor=5)
                LogScreenshot.fLogScreenshot( message = f"Simulation Setup Started - clicked on Simulation setup",
                        pass_ = True, log = True, screenshot = True)
                try:
                    self.SimulationSetupHelperclass.process_Sim_input_row_SimulationSetup(row_data)
                    # self.base.click("Result1link",UnivWaitFor=10)
                except Exception as e:
                    LogScreenshot.fLogScreenshot(message= f"Simulation setup is completed")
                
                #THERE IS A CHANGE IN SIMULATION PAGE THAT WAS NOT THERE IN SIMULATION PAGE BEFORE TEST ENVI- HENCE 
                # THIS NEEDS BE IMPLEMENTED
                try:
                    # Results Validation Logic
                    self.SimresultHelper.validate_sim_results(datafile, row_data, LogScreenshot, tc_status)
                    LogScreenshot.fLogScreenshot(message="Results validation is complete", pass_=True, log=True, screenshot=True)        

                except Exception as e:
                        LogScreenshot.fLogScreenshot( message = f"Error in Generating results : {e}",
                            pass_ = False, log = True, screenshot = True) 
                        tc_status.append("FAIL") 
                self.base.click("CloseResult", UnivWaitFor=8)
                LogScreenshot.fLogScreenshot(message=f"Closed the Result Page ",
                                        pass_=True, log=True, screenshot=True)
            
        tc_status.append("PASS")
        # self.base.switchout()
            # logout and return to login page
            # self.loginpage.logout() 

        #Close the current browser window
        self.driver.quit()
        LogGen.loggen().info(f"- {testcase} completed")

        if "FAIL" in tc_status:
            assert False
            # raise enter message here
        else:
            assert True
