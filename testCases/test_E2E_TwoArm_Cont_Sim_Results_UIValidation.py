
from Helpers.Sim_Design_Helper import Sim_DesignPageHelperfunctions
from Helpers.Sim_Enrollment_Helper import Sim_EnrollmentPageHelperFunctions
from Helpers.Sim_Response_Helper import Sim_ResponsePageHelperFunctions
from Helpers.Sim_SimulationSetup import Sim_SimulationSetupPageHelperFunctions
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from Helpers.LoginPage import LoginPage
from Helpers.Base import Base
import time,os
import pandas as pd
from utilities.reportScreenshot import add_screenshot
import pytest
from utilities.logScreenshot import cLogScreenshot
from Helpers.ExcelHelper import Excel_HelperFunctions
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions


class Test_EndtoEnd_TwoArmCont_Simulation_UIValidation:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArmContinuous_SimResults")
    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()
    
    @pytest.fixture(params=TCList)
    def testcase(self,request):
        return request.param

    @pytest.mark.EndtoEnd
    def test_EndtoEnd_TwoArmContSimulated_workflow_UIValidation(self,testcase,setup,extra,request):
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} started")
        # read the testcase test data file path from wrapper testdata excel file
        path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
        # read the testcase title from wrapper testdata excel file
        title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
        '''
        Read Testdata file and run through the application iteration-wise
        '''
        datafile = pd.read_excel( path, sheet_name = "Testdata" )
        self.driver = setup
        self.driver.get(self.baseURL)      
        # instantiate logscreenshot class
        LogScreenshot = cLogScreenshot(self.driver,extra)
        # Instantiate the Base class
        self.base = Base(self.driver)
        logger = LogGen.loggen()
        # initiate the test case status list
        tc_status = []
        
        self.loginpage = LoginPage(self.driver,extra)
        self.DesignHelper = AD_DesignPageHelperfunctions(self.driver,extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)  
        self.SimulationDesignHelper = Sim_DesignPageHelperfunctions(self.driver,extra)
        self.SimulationResponseHelperclass=Sim_ResponsePageHelperFunctions(self.driver, extra)
        self.SimulationEnrollmentHelperclass=Sim_EnrollmentPageHelperFunctions(self.driver, extra)    
        self.SimulationSetupHelperclass=Sim_SimulationSetupPageHelperFunctions(self.driver, extra)     

        '''
        Clicking on first project  >> click simulate
        Enter input for all pages >> Save & Simulate
        and then verifying field values of simulated Results against test data file
        '''
        time.sleep(3)                  
        print(self.TCList)
        for tc_index in range(len(self.TCList)):
            
            try:
                self.loginpage.complete_login(self.username,self.password,tc_index)
                self.base.click("FirstProject", UnivWaitFor=30)
            except Exception as e:
                LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
                tc_status.append("FAIL")
                
            for row_index, row_data in datafile.iterrows():
                # self.ComputeResults.test_EndtoEnd_TwoArmContResults(tc_index,setup,extra,request)
                
                self.base.click("ResultsPage",UnivWaitFor=10)
                LogScreenshot.fLogScreenshot( message = f"Clicked on Results page",
                        pass_ = True, log = True, screenshot = True)
                # self.base.click("ResultSet1", UnivWaitFor=3)
                self.base.click("Simulatebutton",UnivWaitFor=10)
                self.base.click("CreateInputSetbutton", UnivWaitFor=5)
                
                # Verify Analytical Design Page
                self.base.click("DesignPage", UnivWaitFor=5)
                self.SimulationDesignHelper.verify_elements_AnalyticalDesign(row_index)
                LogScreenshot.fLogScreenshot( message = f"Verify elements on Design page",
                        pass_ = True, log = True, screenshot = True)
                print(" Elements Verification on Design page is completed \n")


                self.base.click("ResponsePage", UnivWaitFor=5)
                self.SimulationResponseHelperclass.verify_elements_AnalyticalResponse(row_index)
                LogScreenshot.fLogScreenshot( message = f"Verify elements on Response page",
                        pass_ = True, log = True, screenshot = True)
                print(" Elements Verification on Response page is completed \n")
                
                self.base.click("EnrollmentPage", UnivWaitFor=5)
                self.base.click("EnrollmentToggle", UnivWaitFor=10)
                LogScreenshot.fLogScreenshot( message = f"Toggled Enrollment",
                        pass_ = True, log = True, screenshot = True)
                # self.base.clickMultipleTimesOnElement("Addbutton", 1)
                self.SimulationEnrollmentHelperclass.verify_elements_AnalyticalEnrollment(tc_index)
                LogScreenshot.fLogScreenshot( message = f"Verify elements on Enrollment page",
                        pass_ = True, log = True, screenshot = True)
                print(" Elements Verification on Enrollment page is completed \n" )

                self.base.click("SimulationSetuplink", UnivWaitFor=5)
                self.SimulationSetupHelperclass.verify_elements_SimulationSetup(tc_index)
                LogScreenshot.fLogScreenshot( message = f"Verify elements on Simulation Setup page",
                        pass_ = True, log = True, screenshot = True)
                self.base.click("Savebutton", UnivWaitFor=5)
                LogScreenshot.fLogScreenshot(message="Clicked on Save button", pass_=True, log=True, screenshot=True)
                self.base.click("SaveSimulate", UnivWaitFor=5)
                LogScreenshot.fLogScreenshot(message="Clicked on Save&Simulate button", pass_=True, log=True, screenshot=True)
                self.base.click("Simulatebutton", UnivWaitFor=10)
                LogScreenshot.fLogScreenshot(message="Clicked on Simulatebutton button", pass_=True, log=True, screenshot=True)        
                # self.base.click("ResultSet1", UnivWaitFor=5)     
                print(" Elements Verification on Simulation page is completed")
                self.base.click("Result1link",UnivWaitFor=10)
            
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
