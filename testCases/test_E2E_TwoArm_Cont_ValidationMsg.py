from Helpers.NewInputHelper import NewInputHelper
from Helpers.ValidationMsg_Helper import ValidationMessageVerifier
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


class Test_EndtoEnd_TwoArmCont_ComputeResults:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserName()
    password = ReadConfig.getPassword()
    wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArmContinuous_ValidationMsg")
    # import the wrapper testdata file
    TSFile = pd.read_excel(wrapperTestData)
    # find the test cases that are to be run
    TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()

    @pytest.fixture(params=TCList)
    def testcase(self, request):
        return request.param

    @pytest.mark.EndtoEnd
    def test_EndtoEnd_TwoArmCont_ComputeResults(self, testcase, setup, extra, request):
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} started")
        path = self.TSFile.loc[self.TSFile['TC_ID'] == testcase]["FilePath"].to_list()[0]
        title = self.TSFile.loc[self.TSFile['TC_ID'] == testcase, 'Title'].to_list()[0]

        datafile = pd.read_excel(path, sheet_name="Testdata")
        self.driver = setup
        self.driver.get(self.baseURL)
        LogScreenshot = cLogScreenshot(self.driver, extra)
        self.base = Base(self.driver)
        logger = LogGen.loggen()
        tc_status = []
        self.loginpage = LoginPage(self.driver, extra)
        self.ProjectandPlancreation = PlanCreationHelper(self.driver, extra)
        self.DesignHelper = AD_DesignPageHelperfunctions(self.driver, extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.NewinputCreation = NewInputHelper(self.driver, extra)
        self.verifier = ValidationMessageVerifier(self.driver, extra)

        time.sleep(3)
        print(self.TCList)
        for tc_index in range(len(self.TCList)):
            try:
                self.loginpage.complete_login(self.username, self.password, tc_index)
                print("login successful")
                self.base.click("FirstProject", UnivWaitFor=30)
                self.base.click("InputSection", UnivWaitFor=10)
                self.base.click("InputSet_link", UnivWaitFor=10)
                print("Clicked on InputSection successful")
                LogScreenshot.fLogScreenshot(message="Clicked on input set", pass_=True, log=True, screenshot=True)
            except Exception as e:
                LogScreenshot.fLogScreenshot(message=f"Error in creating input and selecting dropdowns Input: {e}", pass_=False, log=True, screenshot=True)
            # try:
            tests = [
                {
                    'pre_validation_steps': [
                        {'action': 'click', 'element_locator': 'DesignPage'},
                        {'action': 'click', 'element_locator': 'Type1ErrorRB'}
                    ],
                    'validations': [
                        {'locator': 'AllocationRatioTB', 'invalid_input': '', 'expected_msg_locator' :'Designs_AllocationRatio_ReqValMsg','expected_message' :'Allocation Ratio is required.'},
                        # {'locator': 'PowerTB', 'invalid_input': '', 'expected_msg_locator': 'TwoArmContPower_ReqValMsg', 'expected_message': 'Power is required.'},
                    ]
                }
            ]
            for test in tests:
            # Pre-validation steps
                for step in test['pre_validation_steps']:
                    element = self.base.findElement(step['element_locator'])
                    element.click()
            for validation in test['validations']:
                self.base.ClearTextboxandPressTab(validation['locator'])
                LogScreenshot.fLogScreenshot(message=f"Cleared the textbox", pass_=True, log=True, screenshot=True)
            # element.clear()
            # self.verifier.run_validationtests(tests)
            expected_valmsg=self.base.get_text(validation['expected_msg_locator'])
            print(expected_valmsg)
            print( validation['expected_message'])
            if expected_valmsg == validation['expected_message']:
                print(f"Validation message for {validation['locator']} does match. Expected: {validation['expected_message']} and Found: {expected_valmsg}")
                LogScreenshot.fLogScreenshot(message=f"{validation['locator']} does match. Expected: {validation['expected_message']} and Found: {expected_valmsg}", pass_=True, log=True, screenshot=True)
            else:
                LogScreenshot.fLogScreenshot(message=f"Error in validating error messages: {e}", pass_=False, log=True, screenshot=True)

            tc_status.append("PASS")
            self.base.switchout()

        self.driver.quit()
        LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} completed")

        if "FAIL" in tc_status:
            assert False
        else:
            assert True







# ---------------------------------------------------------------------------------------------------------
# class Test_EndtoEnd_TwoArmCont_ComputeResults:

#     baseURL = ReadConfig.getApplicationURL()
#     username = ReadConfig.getUserName()
#     password = ReadConfig.getPassword()
#     wrapperTestData = ReadConfig.getwrapperTD("E2E_TwoArmContinuous_ValidationMsg")
#     # import the wrapper testdata file
#     TSFile = pd.read_excel(wrapperTestData)
#     # find the test cases that are to be run
#     TCList = TSFile.loc[TSFile['Execute']==1,'TC_ID'].tolist()
    
#     @pytest.fixture(params=TCList)
#     def testcase(self,request):
#         return request.param

#     @pytest.mark.EndtoEnd
#     def test_EndtoEnd_TwoArmCont_ComputeResults(self,testcase,setup,extra,request):
#         LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} started")
#         # read the testcase test data file path from wrapper testdata excel file
#         path = self.TSFile.loc[self.TSFile['TC_ID']==testcase]["FilePath"].to_list()[0]
#         # read the testcase title from wrapper testdata excel file
#         title = self.TSFile.loc[self.TSFile['TC_ID']==testcase,'Title'].to_list()[0]
#         '''
#         Read Testdata file and run through the application iteration-wise
#         '''
#         datafile = pd.read_excel( path, sheet_name = "Testdata" )
#         # dataFile1= pd.read_excel( path, sheet_name = "Teststastic-t" )
#         # dataFile2= pd.read_excel( path, sheet_name = "Teststastic-z" )

#         self.driver = setup

#         self.driver.get(self.baseURL)

#         # instantiate logscreenshot class
#         LogScreenshot = cLogScreenshot(self.driver,extra)

#         # Instantiate the Base class
#         self.base = Base(self.driver)

#         logger = LogGen.loggen()

#         # initiate the test case status list
#         tc_status = []
        
#         # Initialize the LoginPage instance
#         self.loginpage = LoginPage(self.driver,extra)
#         self.ProjectandPlancreation = PlanCreationHelper(self.driver,extra)
#         self.DesignHelper = AD_DesignPageHelperfunctions(self.driver,extra)
#         self.functionsforexcel = Excel_HelperFunctions(self.driver, extra) 
#         self.NewinputCreation=  NewInputHelper(self.driver, extra) 
#         self.verifier= ValidationMessageVerifier(self.driver, extra)

#         '''
#         New Project > create new inputs in iteration > Enter fields from Test data file > 
        
#         '''
#         time.sleep(3)                  
#         print(self.TCList)
#         for tc_index in range(len(self.TCList)):
#             try:
#                 self.loginpage.complete_login(self.username, self.password,tc_index)
#                 print("login succesful")
#                 self.base.click("FirstProject", UnivWaitFor=30)
#                 self.base.click("InputSection", UnivWaitFor=10)
#                 self.base.click("InputSet_link", UnivWaitFor=10)
#                 print("Clicked on InputSection succesful")
#                 LogScreenshot.fLogScreenshot( message = f"Clicked on inputset",
#                          pass_ = True, log = True, screenshot = True)
                
#             #     self.ProjectandPlancreation.new_project_and_plan_creation("Two Arm","Continuous")
#             #     LogScreenshot.fLogScreenshot( message = f"Created TwoArm Plan",
#             #                 pass_ = True, log = True, screenshot = True)
#             #     print("Plan created succesfully")  
#             # except Exception as e:
#             #     LogScreenshot.fLogScreenshot( message = f"Error in test case {self.TCList}: {e}, Unable to create plan",
#             #             pass_ = False, log = True, screenshot = True)
#             # try:
#             #     # Perform actions on the input page based on current row_data
#             #     self.NewinputCreation.create_new_inputSet(iter=1,rowdata=1)  
#             #     print("creating input and Selecting dropdowns  \n") 
#             #     LogScreenshot.fLogScreenshot( message = f"Created New input",
#             #                 pass_ = True, log = True, screenshot = True)              
#             except Exception as e:
#                 LogScreenshot.fLogScreenshot( message = f"Error in creating input and selecting dropdowns Input: {e}",
#                     pass_ = False, log = True, screenshot = True)   
            
#                 # tests = [
#                 #     {
#                 #         'pre_validation_steps': [
#                 #             {'action': 'click', 'element_locator': 'DesignPage'} ,
#                 #             {'action': 'click', 'element_locator': ' Type1ErrorRB'}
#                 #         ],
#                 #         'validations': [
#                 #             {'locator': 'SampleSizeTB', 'invalid_input': '', 'Designs_SampleSize_ReqValMsg': 'Sample Size is required.'},
#                 #             {'locator': 'AllocationRatioTB', 'invalid_input': '', 'Designs_AllocationRatio_ReqValMsg': 'Allocation Ratio is required.'},
#                 #             {'locator': 'PowerTB', 'invalid_input': '', 'TwoArmContPower_ReqValMsg': 'Power is required.'},
#                 #             {'locator': 'MeanTreatmentTB', 'invalid_input': '', 'TwoArmContMeanTretmnt_ReqValMsg': 'Mean Treatment is required.'},
#                 #             {'locator': 'MeanControlTB', 'invalid_input': '', 'TwoArmContMeanCont_ReqValMsg': 'Mean Control is required.'},
#                 #             {'locator': 'StandardDeviationTB', 'invalid_input': '', 'TwoArmContStdDev_ReqValMsg': 'Standard Deviation is required.'},
#                 #             {'locator': 'ProbabilityDropoutTB', 'invalid_input': '', 'TwoArmContProbDropout_ReqValMsg': 'Probability of Dropout is required.'},
                                          
#                 #         ]
#                 #     }
#                 # tests = [
#                 #     {
#                 #         'pre_validation_steps': [
#                 #             {'action': 'click', 'element_locator': 'DesignPage'},
#                 #             {'action': 'click', 'element_locator': 'Type1ErrorRB'}
#                 #         ],
#                 #         'validations': [
#                             # {'locator': 'SampleSizeTB', 'invalid_input': '', 'expected_message': 'Sample Size is required.'},
#                         #     {'locator': 'AllocationRatioTB', 'invalid_input': '', 'expected_message': 'Allocation Ratio is required.'},
#                                 # {'locator': 'PowerTB', 'invalid_input': '', 'TwoArmContPower_ReqValMsg': 'Power is required.'},
#                         #     {'locator': 'MeanTreatmentTB', 'invalid_input': '', 'expected_message': 'Mean Treatment is required.'},
#                         #     {'locator': 'MeanControlTB', 'invalid_input': '', 'expected_message': 'Mean Control is required.'},
#                         #     {'locator': 'StandardDeviationTB', 'invalid_input': '', 'expected_message': 'Standard Deviation is required.'},
#                         #     {'locator': 'ProbabilityDropoutTB', 'invalid_input': '', 'expected_message': 'Probability of Dropout is required.'},
#                 #         ]
#                 #     }
#                 # ]

                    
#                     # {
#                     #     'pre_validation_steps': [
#                     #         {'action': 'click', 'element_locator': 'ResponsePage'},
#                     #         {'action': 'select_by_visible_text', 'element_locator': ('id', 'TestStasticDropddown'), 'text': 'SampleSize'}
#                     #     ],
#                     #     'validations': [
#                     #         {'field_locator': ('id', 'MeanTreatmentTB'), 'invalid_input': 'invalid_email', 'expected_message': 'Invalid email address'},
#                     #         {'field_locator': ('id', 'MeanControlTB'), 'invalid_input': '', 'expected_message': 'Password is required'},
#                     #         {'field_locator': ('id', 'ProbabilityDropoutTB'), 'invalid_input': 'short', 'expected_message': 'Password must be at least 6 characters long'},
#                     #         {'field_locator': ('id', 'SdcontrolTB'), 'invalid_input': 'short', 'expected_message': 'Password must be at least 6 characters long'},
#                     #         {'field_locator': ('id', 'SDTreatmentTB'), 'invalid_input': 'short', 'expected_message': 'Password must be at least 6 characters long'},
#                     #     ]
#                     # },
#                     # {
#                     #     'pre_validation_steps': [
#                     #         {'action': 'click', 'element_locator': 'EnrollmentPage'},
#                     #         {'action': 'click', 'element_locator': 'EnrollmentToggle'},
#                     #         {'action': 'click', 'element_locator': 'Addbutton'},
#                     #     ],
#                     #     'validations': [
#                     #         {'field_locator': ('id', 'AvgSubTB'), 'invalid_input': 'invalid_email', 'expected_message': 'Invalid email address'},
#                     #         {'field_locator': ('id', 'StartAtTimeTB2'), 'invalid_input': '', 'expected_message': 'Password is required'},
#                     #         {'field_locator': ('id', 'AvgSubTB2'), 'invalid_input': 'short', 'expected_message': 'Password must be at least 6 characters long'},
#                     #     ]
#                     # }
#                 # ]
#             try:
#                 tests = [
#                     {
#                         'pre_validation_steps': [
#                             {'action': 'click', 'element_locator': 'DesignPage'},
#                             {'action': 'click', 'element_locator': 'Type1ErrorRB'}
#                         ],
#                         'validations': [
#                             {'locator': 'PowerTB', 'invalid_input': '', 'excpected_msg_locator':'TwoArmContPower_ReqValMsg','expected_message' :'Power is required.'},
#                         ]
#                     }
#                 ]
                
#                 self.verifier.run_validationtests(tests) 
#                 LogScreenshot.fLogScreenshot(message=f"Validating error msg is successful", pass_=True, log=True, screenshot=True)
#             except Exception as e:
#                     LogScreenshot.fLogScreenshot(message=f"Error in validating error msgs: {e}", pass_=False, log=True, screenshot=True)
    
            
#         tc_status.append("PASS")
#         self.base.switchout()
#             # logout and return to login page
#             # self.loginpage.logout() 

#         #Close the current browser window
#         self.driver.quit()
#         LogGen.loggen().info(f"Two-Arm-Continuous - {testcase} completed")

#         if "FAIL" in tc_status:
#             assert False
#             # raise enter message here
#         else:
#             assert True

