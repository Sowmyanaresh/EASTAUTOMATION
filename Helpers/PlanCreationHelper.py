import time
from Helpers.Base import Base 
from utilities.readProperties import ReadConfig
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.common.by import By
import pandas as pd
import tkinter as tk
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.by import By
import functools
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import string
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.logScreenshot import cLogScreenshot
from selenium.common.exceptions import NoSuchElementException

class PlanCreationHelper:    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)         
        self.env = ReadConfig.getEnvironmenttype()
       
    def new_project_and_plan_creation(self,StudyObjective,EndpointType,TargetPopulation,ControlArm,TreatmentArm,EndpointName,BetterResponse,FollowUpTime):
        '''
        User should able to reach to plan page before calling this method and this method enters all mandatory fields on plan page on basis on providing study objective and endpointtype
        '''
        try:
            self.base.click("Project_NewProjectButton",UnivWaitFor = 20)
            self.LogScreenshot.fLogScreenshot( message = f"Clicking On New Project Button :",
                pass_ = True, log = True, screenshot = True)
            projectNameTextBox = 'Project_ProjectNameTextBox'
            self.base.input_text_random(projectNameTextBox,UnivWaitFor=3)
            self.LogScreenshot.fLogScreenshot( message = f"Enter The Project Name :",
                pass_ = True, log = True, screenshot = True)
            self.base.click("Project_TimeUnitDropdownClick",UnivWaitFor = 3)
            self.LogScreenshot.fLogScreenshot( message = f"Click the Time Unit Dropdown:",
                pass_ = True, log = True, screenshot = True)
            self.base.click("Project_TimeUnitDropdownValueDay",UnivWaitFor = 3)
            self.LogScreenshot.fLogScreenshot( message = f"select the Time Unit Dropdown Value :",
                pass_ = True, log = True, screenshot = True)
            self.base.input_text_presstab("Plans_ProjectDescription","Description of the project")
            # time.sleep(20)
        except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in creating project : {e}",
                pass_ = False, log = True, screenshot = True) 
        if StudyObjective == "Two Arm Confirmatory":
            try:
                self.base.selectByvisibleText("plans_subjectObjectiveDropdown",StudyObjective,UnivWaitFor = 3)
                self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value:",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True) 
            try:
                self.base.selectByvisibleText("plans_EndPointsType",EndpointType,UnivWaitFor = 3)
                self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value:",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True) 
            try: 
                self.base.input_text_with_ctrlAltDel('plans_TargetPopulation',TargetPopulation,UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Target Population Field value :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel('plans_ControlArms',ControlArm,UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Control Arm Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel('plans_TreatmentArms',TreatmentArm,UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Treatment Arms Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:                
                ####################################
                # Wait for the element to be present and clickable
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="endpointName-0"]'))
                )
                # Clear the existing text if any
                element.clear()
                # Send keys character by character with a slight delay
                for char in EndpointName:
                    element.send_keys(char)
                    time.sleep(0.1)                 
                element.send_keys(Keys.TAB)
                ####################################                
                self.LogScreenshot.fLogScreenshot( message = f"Enter Endpoint Name Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                self.base.selectByvisibleText("betterResponse_EP1", BetterResponse,UnivWaitFor = 3)                
                self.LogScreenshot.fLogScreenshot( message = f"Select Better Response Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel("plans_followUpTimeEP1",FollowUpTime,UnivWaitFor=3)                
                self.LogScreenshot.fLogScreenshot( message = f"Enter Endpoint name Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
        # Click on Create Project button 
        elif StudyObjective == "One Arm Exploratory / Confirmatory":
            try:
                self.base.selectByvisibleText("plans_subjectObjectiveDropdown",StudyObjective,UnivWaitFor = 2)
                self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value:",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True) 
            try:
                self.base.selectByvisibleText("plans_EndPointsType",EndpointType,UnivWaitFor = 2)
                self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value:",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True)  
            try: 
                self.base.input_text_with_ctrlAltDel('plans_TargetPopulation',TargetPopulation,UnivWaitFor=2)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Target Population Field value :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel('plans_TreatmentArms',TreatmentArm,UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Treatment Arms Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try: 
                               
                ####################################
                # Wait for the element to be present and clickable
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="endpointName-0"]'))
                )
                # Clear the existing text if any
                element.clear()
                # Send keys character by character with a slight delay
                for char in EndpointName:
                    element.send_keys(char)
                    time.sleep(0.1)                 
                element.send_keys(Keys.TAB)
                ####################################                
                self.LogScreenshot.fLogScreenshot( message = f"Enter Endpoint Name Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                
                self.base.selectByvisibleText("betterResponse_EP1", BetterResponse,UnivWaitFor = 2)                
                self.LogScreenshot.fLogScreenshot( message = f"Select Better Response Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
                
            try:
                if EndpointType=="Time to Event":
                    pass
                else:
                    self.base.input_text_with_ctrlAltDel("plans_followUpTimeEP1",FollowUpTime,UnivWaitFor=2)                
                    self.LogScreenshot.fLogScreenshot( message = f"Enter Endpoint name Field value:",
                        pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
        try:
              self.base.click("newProjectCreationButton",UnivWaitFor=5)
              self.LogScreenshot.fLogScreenshot( message = f"Created New project Successfully :",
                    pass_ = True, log = True, screenshot = True) 
        except Exception as e:
               self.LogScreenshot.fLogScreenshot( message = f"Error in clicking on create project : {e}",
                    pass_ = False, log = True, screenshot = True) 
               
    def plan_fields_validation(self):
        self.base.PressTab("plans_subjectObjectiveDropdown")
        time.sleep(3)
        self.LogScreenshot.fLogScreenshot( message = f"Press tab without selecting study objective dropdown value:",
        pass_ = True, log = True, screenshot = True)

        StudyObjActual= self.base.get_text("Plans_StudyObjectiveValidation1")
        
        StudyobjExpected= 'Study Objective is required.'
        if StudyObjActual==StudyobjExpected:
            try:
                self.LogScreenshot.fLogScreenshot( message = f"Study Objective validation is matching the expected data:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Validation not matching {e}",
                    pass_ = False, log = True, screenshot = True)
       # self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Two Arm",UnivWaitFor = 10)
        self.base.selectByvisibleText("Designs_StudyObjectiveDD","Two Arm")  
        self.LogScreenshot.fLogScreenshot( message = f"Selected study objective dropdown value:",
        pass_ = True, log = True, screenshot = True)
        
        self.base.click("Plans_FollowupTimeCheckbox")   
        self.LogScreenshot.fLogScreenshot( message = f"Follow-up time checkbox unchecked:",
        pass_ = True, log = True, screenshot = True)     
        self.base.click("Plans_ToggleUseStratification_Card1")
        for button in range (3):
            self.base.click("Plans_AddLevelbutton")
            self.LogScreenshot.fLogScreenshot( message = f"Clicked Add Level button for maximum times:",
            pass_ = True, log = True, screenshot = True)
        
    def inputUseStratificationFields(self):
        self.base.input_text("Plans_FactorInputFieldCardOne", "FctName")
        self.base.input_text("Plans_Level1InputFieldCard1","levl1data")
        self.base.input_text("Plans_Level2InputFieldCard1","leve2data")
        self.base.input_text("Plans_Level3InputFieldCard1","lev3da")
        self.base.input_text("Plans_Level4InputFieldCard1","lvl4")
        self.base.input_text("Plans_Level5InputFieldCard1","lvl5")
        self.base.input_text("Plans_FollowupTimeTextbox", "1")

    def switch_ON_OffUseStratification(self):
        try:
            self.base.click("Plans_ToggleUseStratification_Card1",UnivWaitFor=2)
            self.base.click("Plans_FollowupTimeCheckbox",UnivWaitFor=2)   
            self.base.clickMultipleTimesOnElement("Plans_AddLevelbutton",3)

        except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in toggling and adding levels {e}",
                    pass_ = False, log = True, screenshot = True) 

    def clearTextboxbasedonEndpoint(self,studyobjective,endpointtype,secondEndpointtype=None):
        '''
        This method is to clear text boxes based on Endpoint
        '''
        if studyobjective == "Two Arm": 
            try: 
                self.base.pressTabforInputfield('plans_TargetPopulation',UnivWaitFor=1)
                self.base.pressTabforInputfield('plans_ControlArms',UnivWaitFor=1)
                self.base.pressTabforInputfield('plans_TreatmentArms',UnivWaitFor=1)
                self.base.pressTabforInputfield('plans_EndPointsName',UnivWaitFor=1)
                while endpointtype == 'Time to Event':
                    self.base.click("Plans_FollowupTimeCheckbox",UnivWaitFor=1)
                    self.base.pressTabforInputfield("Plans_FollowupTimeTextboxTTE",UnivWaitFor=2)
                    break
                else:  
                    self.base.pressTabforInputfield('Plans_FollowupTimeTextbox',UnivWaitFor=1)
                    
                    self.LogScreenshot.fLogScreenshot( message = f"Clearing all the Text fields is succesfull for the EP : {endpointtype}",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in clearing the fields : {e}",
                    pass_ = False, log = True, screenshot = True) 
               
        elif studyobjective == "Multiple Arm Confirmatory":
            #self.base.click("Plans_StudyObjectAlertPopYes",UnivWaitFor=2)
            Addarmbutton = "Plans_AddArmButton"
            if self.base.element_is_enabled(Addarmbutton)==True:
                self.base.click(Addarmbutton)

            try: 
                self.base.ClearTextboxandPressTab('plans_TargetPopulation',UnivWaitFor=1)
                # self.base.pressTabforInputfield('plans_ControlArms',UnivWaitFor=1)
                # self.base.pressTabforInputfield('plans_TreatmentArms',UnivWaitFor=1)
                self.base.ClearTextboxandPressTab('plans_EndPointsName',UnivWaitFor=1)
                self.base.ClearTextboxandPressTab('Plans_FollowupTimeTextbox',UnivWaitFor=1)
                self.base.ClearTextboxandPressTab('Plans_ControlArmsField')
                self.base.ClearTextboxandPressTab('Plans_Arm1Field')
                self.base.ClearTextboxandPressTab('Plans_Arm2Field')
                self.base.ClearTextboxandPressTab('Plans_Arm3Field')
                self.base.ClearTextboxandPressTab('Plans_Arm4Field')
                self.LogScreenshot.fLogScreenshot( message = f"Clearing all the Text fields is succesfull for the Endpoint : {endpointtype}",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in clearing the fields : {e}",
                    pass_ = False, log = True, screenshot = True) 

        elif studyobjective == "Dose Finding":
            try:
                self.base.selectByvisibleText("plans_subjectObjectiveDropdown",studyobjective,UnivWaitFor = 2)
                self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value: {studyobjective}",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True) 
            try:
                self.base.selectByvisibleText("plans_EndPointsType",endpointtype,UnivWaitFor = 2)
                self.LogScreenshot.fLogScreenshot( message = f"Select End Point Type dropdown value:",
                pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                pass_ = False, log = True, screenshot = True) 
            try: 
                self.base.input_text_with_ctrlAltDel('plans_TargetPopulation',UnivWaitFor=1)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Target Population Field value :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)  
            try:
                self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"EP1",UnivWaitFor=1)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Endpoint name Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
    
    def TimetoEvent_Plan(self):
        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Two Arm",UnivWaitFor =2 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Two Arm",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Study Objective : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType","Time to Event",UnivWaitFor =5 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Time to Event Endpoint type",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Endpoint Type : {e}",
            pass_ = False, log = True, screenshot = True) 
        try: 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_ControlArms',"ControlArm",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_TreatmentArms',"Treatment",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"TTE EP1",UnivWaitFor=1)
            self.LogScreenshot.fLogScreenshot( message = f"Entering all the Mandatory fields such as Target Population,Control Arm ,Treatment Arm and Endpoint name Field value is succesfull:",
                pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in entering the mandatory fields : {e}",
                pass_ = False, log = True, screenshot = True) 

    def Binary_Plan(self):
        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Two Arm",UnivWaitFor =2 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Two Arm",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Study Objective : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType","Binary",UnivWaitFor =5 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Time to Event Endpoint type",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Endpoint Type : {e}",
            pass_ = False, log = True, screenshot = True) 
        try: 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_ControlArms',"ControlArm",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_TreatmentArms',"Treatment",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"TTE EP1",UnivWaitFor=1)
            self.LogScreenshot.fLogScreenshot( message = f"Entering all the Mandatory fields such as Target Population,Control Arm ,Treatment Arm and Endpoint name Field value is succesfull:",
                pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in entering the mandatory fields : {e}",
                pass_ = False, log = True, screenshot = True) 
    
    def Continuous_Plan(self):
        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Two Arm",UnivWaitFor =2 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Two Arm",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Study Objective : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType","Continuous",UnivWaitFor =5 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Time to Event Endpoint type",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Endpoint Type : {e}",
            pass_ = False, log = True, screenshot = True) 
        try: 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_ControlArms',"ControlArm",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_TreatmentArms',"Treatment",UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"TTE EP1",UnivWaitFor=1)
            self.LogScreenshot.fLogScreenshot( message = f"Entering all the Mandatory fields such as Target Population,Control Arm ,Treatment Arm and Endpoint name Field value is succesfull:",
                pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in entering the mandatory fields : {e}",
                pass_ = False, log = True, screenshot = True) 

    def Continuous_PlanMultiArm(self):
        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Multiple Arm Confirmatory",UnivWaitFor =2 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Two Arm",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Study Objective : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType","Continuous",UnivWaitFor =5 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Time to Event Endpoint type",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Endpoint Type : {e}",
            pass_ = False, log = True, screenshot = True) 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"Continuous EP1",UnivWaitFor=1)
            try: 
                self.LogScreenshot.fLogScreenshot( message = f"Entering Target Population & Ep value is succesful :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)  
            try: 
                self.base.input_text_with_ctrlAltDel('Plans_Arm1Field',"ARM1",UnivWaitFor=1)
                self.base.input_text_with_ctrlAltDel('Plans_Arm2Field',"ARM2",UnivWaitFor=1)
                self.LogScreenshot.fLogScreenshot( message = f"Enterin Arm1 & Arm 2 Field value is succesfull",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"field values are not entered : {e}",
                    pass_ = False, log = True, screenshot = True) 

    def Binary_PlanMultiArm(self):
        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Multiple Arm Confirmatory",UnivWaitFor =2 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Two Arm",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Study Objective : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType","Binary",UnivWaitFor =5 )
            self.LogScreenshot.fLogScreenshot( message = f"Selected Time to Event Endpoint type",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Unable to select Endpoint Type : {e}",
            pass_ = False, log = True, screenshot = True) 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"Continuous EP1",UnivWaitFor=1)
            try: 
                self.LogScreenshot.fLogScreenshot( message = f"Entering Target Population & Ep value is succesful :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)  
            try: 
                self.base.input_text_with_ctrlAltDel('Plans_Arm1Field',"ARM1",UnivWaitFor=1)
                self.base.input_text_with_ctrlAltDel('Plans_Arm2Field',"ARM2",UnivWaitFor=1)
                self.LogScreenshot.fLogScreenshot( message = f"Enterin Arm1 & Arm 2 Field value is succesfull",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"field values are not entered : {e}",
                    pass_ = False, log = True, screenshot = True) 

    def Continuous_PlanDoseFinding(self):

        self.base.click("Plans_leftpanellink")
        try:
            self.base.selectByvisibleText("plans_subjectObjectiveDropdown","Dose Finding",UnivWaitFor = 2)
            self.LogScreenshot.fLogScreenshot( message = f"Select study objective dropdown value: ",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
            pass_ = False, log = True, screenshot = True) 
        try:
            self.base.selectByvisibleText("plans_EndPointsType",'Continuous',UnivWaitFor = 2)
            self.LogScreenshot.fLogScreenshot( message = f"Select End Point Type dropdown value:",
            pass_ = True, log = True, screenshot = True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in selecting Endpoint {e}",
            pass_ = False, log = True, screenshot = True) 
            self.base.input_text_with_ctrlAltDel('plans_TargetPopulation','Target Pop',UnivWaitFor=1)
            self.base.input_text_with_ctrlAltDel('plans_EndPointsName',"Continuous EP1",UnivWaitFor=1)
            try: 
                self.LogScreenshot.fLogScreenshot( message = f"Entering Target Population & Ep value is succesful :",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 

    def Enable_StratificationinPlans(self):
            try:
                self.base.click("Plans_UseStratificationToggleButton",UnivWaitFor = 6)
                
                self.base.click("Plans_AddLevelbutton",UnivWaitFor=2)  
                self.base.click("Plans_AddLevelbutton",UnivWaitFor=2)  
                self.base.click("Plans_AddLevelbutton",UnivWaitFor=2) 
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
 
            try:
                self.base.input_text('Plans_FactorInputFieldCardOne',"Factory",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Factory  Field value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
                  
            try:
                #Level1=dataFile.loc[i,'Level1Field']
                self.base.input_text('Plans_Level1InputFieldCard1',"Level1",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Level 1 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                #Level2=dataFile.loc[i,'Level2Field']
                self.base.input_text('Plans_Level2InputFieldCard1',"Level2",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Level 2 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                #Level2=dataFile.loc[i,'Level2Field']
                self.base.input_text('Plans_Level3InputFieldCard1',"Level3",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Level 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                #Level2=dataFile.loc[i,'Level2Field']
                self.base.input_text('Plans_Level4InputFieldCard1',"Level4",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Level 4 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                #Level2=dataFile.loc[i,'Level2Field']
                self.base.input_text('Plans_Level5InputFieldCard1',"Level5",UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Level 5 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 

    def Enable_RepeatedMeasuresPlans(self):
            try:
                self.base.click("Plans_RM_Toggle",UnivWaitFor = 6)
                self.base.click("Plans_AddVisitbutton",UnivWaitFor=2)  
                self.base.click("Plans_AddVisitbutton",UnivWaitFor=2)  
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel("Plans_FollowUpContinuous","10",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Follow-up Time Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                self.base.input_text("Plans_RM_Visit1","2",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 1 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit2","4",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 2 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit3","6",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit4","8",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                self.base.input_text("Plans_RM_Visit5","9",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)            

    def Enable_RepeatedMeasuresPlans(self):
            try:
                self.base.click("Plans_RM_Toggle",UnivWaitFor = 6)
                self.base.click("Plans_AddVisitbutton",UnivWaitFor=2)  
                self.base.click("Plans_AddVisitbutton",UnivWaitFor=2)  
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text_with_ctrlAltDel("Plans_FollowUpContinuous","10",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Follow-up Time Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                self.base.input_text("Plans_RM_Visit1","2",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 1 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit2","4",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 2 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit3","6",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True) 
            try:
                self.base.input_text("Plans_RM_Visit4","8",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)
            try:
                self.base.input_text("Plans_RM_Visit5","9",UnivWaitFor = 6)
                self.LogScreenshot.fLogScreenshot( message = f"Enter Visit 3 Field Value:",
                    pass_ = True, log = True, screenshot = True)
            except Exception as e:
                self.LogScreenshot.fLogScreenshot( message = f"Error in logging in : {e}",
                    pass_ = False, log = True, screenshot = True)

