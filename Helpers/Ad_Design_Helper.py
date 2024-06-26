import os
import time

import pandas as pd
from Helpers.Base import Base 
from Helpers.ExcelHelper import Excel_HelperFunctions
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Helpers.NewInputHelper import NewInputHelper
from selenium.webdriver.common.by import By
import urllib.parse
from selenium.webdriver.common.keys import Keys
import re
# import pyautogui

class AD_DesignPageHelperfunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.newinputcreation = NewInputHelper(self.driver,extra)
    
    def clickOnSaveButton(self):
        self.base.click("Project_SaveButtonOnNewProjectWindow")
        time.sleep(3)
        
    def ToggleAssurance_POS(self,UnivWaitFor=0):
        self.base.click("IncludeAssurance",UnivWaitFor=5)
        time.sleep(2)

    def verify_elements_WithAccural(self):
            """
                Helper function to verify the presence, visibility, disabled state, and text content of a web element.
            Returns:
                bool: True if the element is present, visible, disabled, and contains the expected text; False otherwise.
            """
            elements= ['AssuranceTextbox',
                        'PriorDistributionForDD',
                        'eDeltaTB',
                        'sDeltaTB',
                        'Assur_InputmethodDD',
                        'DistributionMethodDD'
                        ]
            for element_id in elements:
                try:
                    # Find the element by its ID
                    element = self.base.verifyelement_displayed(element_id)
                    # Check if the element is displayed
                    if element:
                        print(f"Element '{element_id}' is displayed on the webpage.")
                    else:
                        print(f"Element '{element_id}' is not displayed on the webpage.")
                
                except NoSuchElementException:
                    print(f"Element '{element_id}' not found on the webpage.")

            Disabledelements= ['AssuranceTextbox',
                        'PriorDistributionForDD']
            try:
                for elementid in Disabledelements:
                    if self.base.isdisabled(elementid):
                        print(elementid)
                        return True
            except Exception as e:
                    print(f"Element '{elementid}' is not disabled on the webpage.")
            try:
                elementtext=self.base.get_text(elementid)
                if elementtext=="Computed":
                        print(elementtext)
                        return True
            except Exception as e:
                    print(f"Element '{element_id}' text is not as expected on the webpage.")    

    def compare_dropdown_options(self, dropdown_id, expected_options):
        try:
            dropdown_options= [] 
            dropdown_options=self.base.ExtractDropdownItems_SelectDropdown(dropdown_id,UnivWaitFor=10)
            # Compare extracted options with expected options
            print("These dropdown options extracted from web page" , dropdown_options)
            if dropdown_options == expected_options:
                print(f"Dropdown options for '{dropdown_options}'match the expected options.")
                self.LogScreenshot.fLogScreenshot( message = f"Dropdown options '{dropdown_options}'{expected_options} match the expected options.",
                pass_ = True, log = True, screenshot = True)
            else:
                print(f"Dropdown options for '{dropdown_options}'do not match the expected options.")
                self.LogScreenshot.fLogScreenshot( message = f"Dropdown options '{dropdown_id}'{expected_options} DO NOT match the expected options.",
                pass_ = False, log = True, screenshot = True)
        except Exception as e:
            print(f"Error occurred while processing dropdown '{dropdown_id}': {str(e)}")
            
            # expected_options_dict = {'Assur_InputmethodDD': ['InputMethodDDOption1', 'InputMethodDDOption2', 'InputMethodDDOption3'],
            #                         'DistributionMethodDD': ['DistributionMethodDDOption1', 'DistributionMethodDDOption2', 'DistributionMethodDDOption3']
            #                             }

            # # try:
            #      self.base.ExtractDropdownItems_SelectDropdown("Assur_InputmethodDD",UnivWaitFor=10)
            #      self.base.ExtractDropdownItems_SelectDropdown("DistributionMethodDD",UnivWaitFor=10)
            # except Exception as e:
            #         print(f"Dropdown items are not matching with expected items.")

    def Select_Superiority(self,Inputmethodtype,value,UnivWaitFor=0):
         self.base.selectByvisibleText("HypothesisDD","Superiority",UnivWaitFor=5)
         self.base.selectByvisibleText("InputMethod",Inputmethodtype)
         self.base.selectByvisibleText("TestStatisticDD",value)
       
    def Select_SuperSuperiority(self,teststastic,UnivWaitFor=0):
        self.base.selectByvisibleText("HypothesisDD","Super Superiority")
        self.base.selectByvisibleText("InputMethod",teststastic)

    def Select_Noninferiority(self,teststastic,UnivWaitFor=0):
        self.base.selectByvisibleText("HypothesisDD","Noninferiority")
        self.base.selectByvisibleText("InputMethod",teststastic)

    def Select_InputMethod(self,Inputmethod,UnivWaitFor=0):
        Inputmethod=['Individual Means','Difference of Means','Standardized Diff. of Means']
        if Inputmethod=='Individual Means':
            self.Select_Superiority('Individual Means','Z')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Individual Means option from the InputMethod dropdown",
                    pass_ = True, log = True, screenshot = True)  
        elif Inputmethod=='Difference of Means':
            self.Select_Superiority('Difference of Means','Z')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Difference of Means option from the InputMethod dropdown",
                    pass_ = True, log = True, screenshot = True)  
        elif Inputmethod=='Standardized Diff. of Means':
                self.Select_Superiority('Standardized Diff. of Means','Z')
                # Enable Assurance
                self.LogScreenshot.fLogScreenshot( message = f"Selected Standardized Diff. of Means option from the InputMethod dropdown",
                        pass_ = True, log = True, screenshot = True) 

    def perform_input_actions(self,iter, row_data, LogScreenshot):
        """
        Perform actions on the input page based on the provided row_data.
        Parameters:
            row_data (pd.Series): Series containing data for the current input iteration.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
        """
        try:
            # Example: Implement actions to interact with the input page using row_data
            self.base.click("Project_InputsLink", UnivWaitFor=15)
            self.newinputcreation.create_new_inputSet(iter,row_data)           
            self.LogScreenshot.fLogScreenshot(message="Clicked on 'Design' option and landed in Design page-perform_input_actions method completed",
                                        pass_=True, log=True, screenshot=True)
            time.sleep(1)
        except Exception as e:
            raise Exception(f"Error selecting dropdowns : {e}")
        
    def process_input_row_generic(self, row_data,WhatToCompute):       
        try:     
            time.sleep(4)     
            self.base.selectByvisibleText("HypothesisDD", row_data['Hypothesis'])         
            # self.fill_input_field('AllocationRatioTB', row_data, 'AllocationRatio', 'Enter The value in Allocation Ratio Field :')
            try:
                    if float(row_data['responseLag']) > 0:
                        self.fill_input_field('ProbabilityDropoutTB', row_data, 'probOfDropout', 'Enter the value on Probability dropout Field')
                        self.LogScreenshot.fLogScreenshot(message=f"Entered value in ProbofDropout", pass_=True, log=True, screenshot=True)                
            except ValueError:
                    print("Invalid value for responseLag:", row_data['responseLag'])

            if WhatToCompute == 'Sample Size':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.base.click("SampleSizeRB", UnivWaitFor=1)                
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')  
            
            elif WhatToCompute == 'Alpha':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.fill_input_field('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')
            
            elif WhatToCompute == 'Power':
                self.base.click("PowerRB", UnivWaitFor=1)
                self.fill_input_field('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')                                
                
            elif WhatToCompute == 'Diff. in Means':
                self.base.click("DiffInMeansRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')
                
            elif WhatToCompute == 'Hazard Ratio':
                self.base.click("HazardRatioRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('SampleSizeTB', row_data,'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field ')     
            
            elif WhatToCompute == 'Ratio of Means':
                self.base.click("DifferenceofMeansRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')     
            else:
                self.LogScreenshot.fLogScreenshot(message=f"Invalid option for WhatToCompute", pass_=False, log=True, screenshot=True)                
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering generic design input DOM{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_generic_MOPR_MOPD(self, row_data,WhatToCompute):       
        try:          
            self.base.selectByvisibleText("HypothesisDD", row_data['Hypothesis'])     
            self.LogScreenshot.fLogScreenshot(message=f"Selected value from Hypothesis dropdown", pass_=True, log=True, screenshot=True)                

            if WhatToCompute == 'Sample Size':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.base.click("SampleSizeRB", UnivWaitFor=1)                
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')  
            elif WhatToCompute == 'Alpha':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')
            elif WhatToCompute == 'Power':
                self.base.click("PowerRB", UnivWaitFor=1)
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')                                
            elif WhatToCompute == 'Diff. in Means':
                self.base.click("DiffInMeansRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')
            elif WhatToCompute == 'Hazard Ratio':
                self.base.click("HazardRatioRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field ')     
            elif WhatToCompute == 'Ratio of Means':
                self.base.click("DifferenceofMeansRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')     

            else:
                self.LogScreenshot.fLogScreenshot(message=f"Invalid option for WhatToCompute", pass_=False, log=True, screenshot=True)                
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering generic input for MOPR / MOPD{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_generic_SingleArm(self, row_data,WhatToCompute):       
        try:          
            # self.base.selectByvisibleText("HypothesisDD", row_data['Hypothesis'])
            if WhatToCompute == 'Sample Size':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.base.click("SampleSizeRB", UnivWaitFor=1)                
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')  

            elif WhatToCompute == 'Alpha':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')
                
            elif WhatToCompute == 'Power':
                self.base.click("PowerRB", UnivWaitFor=1)
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')   

            elif WhatToCompute == 'Hazard Ratio':
                self.base.click("HazardRatioRB", UnivWaitFor=1)
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field ')
            else:
                self.LogScreenshot.fLogScreenshot(message=f"Invalid option for WhatToCompute", pass_=False, log=True, screenshot=True)                
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering generic design inputs{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_enrollement(self, row_data):
        try:
            if (str(int(row_data['includeAccrualDropout']))== '1'):
                self.base.click("Enrollment_leftpanellink",UnivWaitFor = 4)
                self.base.click("EnrollmentToggle", UnivWaitFor=3)
                self.fill_input_field('EnrollmentAvgSubTB', row_data, 'accrualRate', 'Enter The value in accrualRate Field ')
                self.LogScreenshot.fLogScreenshot(message=f"All Enrollment Inputs provided",
                                    pass_=True, log=True, screenshot=True)
                print("accuralrate:", row_data['accrualRate'])
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering enrollment inputs{e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_enrollment_SingleArm(self, row_data):
        try:
            
            self.base.click("Enrollment_leftpanellink",UnivWaitFor = 1)
            # if self.base.isenabled("EnrollmentType"):
            #     self.base.selectByvisibleText("EnrollmentType",row_data,UnivWaitFor = 2)
            # else:
            #     self.LogScreenshot.fLogScreenshot(message=f"EnrollmentType is not enabled, skipping selection.{e}", pass_=False, log=True, screenshot=True)

            self.fill_input_field('studyDuration', row_data, 'studyDuration', 'Enter the value in StudyDuration Field')
            self.fill_input_field('accrualDuration', row_data, 'accrualDuration', 'Enter the value in AccrualDuration Field')
            self.base.PressTab('accrualDuration')
                            
            if (row_data['Test'] == 'Logrank Exponential Distribution'):
                try:
                    if (row_data['dropoutInputMethod'] == 'Hazard Rates'): 
                        print("selected Hazard Rates")
                        self.base.click("dropoutInputMethod", UnivWaitFor=1)
                        print("Clicked on Dropdown method")
                        self.LogScreenshot.fLogScreenshot(message=f"Clicked on Dropdown method",
                                                    pass_=True, log=True, screenshot=True)
            
                        self.base.selectByvisibleText("dropoutInputMethod",'Hazard Rates',UnivWaitFor = 3)
                        self.fill_input_field('dropoutHazardRate', row_data, 'ExponentialDropoutRate', 'Enter The value in dropout-HazardRate Field ')
                        time.sleep(3)
                    elif (row_data['dropoutInputMethod'] == 'Probability of Dropout'): 
                        self.base.selectByvisibleText("dropoutInputMethod",'Probability of Dropout',UnivWaitFor = 2)
                        print("selected Probability of Dropout")
                        self.fill_input_field('dropoutByTime', row_data, 'EnrollmentByTime', 'Enter The value in dropoutByTime Field ')
                        self.fill_input_field('probabilityOfDropout', row_data, 'ProbabilityOfDropout', 'Enter The value in probabilityOfDropout Field ')
                except Exception as e:
                    self.LogScreenshot.fLogScreenshot(message=f"Error in selecting dropout types {e}", pass_=False, log=True, screenshot=True)
    
            self.LogScreenshot.fLogScreenshot(message=f"All Enrollment Inputs provided",
                                        pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering enrollment inputs- Single Arm {e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_SingleArmTTE_Inputmethod(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
                if (row_data['inputMethod'] == 'Hazard Rates') :      
                    self.base.selectByvisibleText("InputMethod", row_data['inputMethod'])   
                    
                    if row_data['WhatToCompute'] == 'Hazard Ratio':
                        self.fill_input_field('hazardRateNull', row_data, 'Hazard_Rate_Control', 'Enter The value in hazardRateNull Field ')
                    elif row_data['WhatToCompute'] != 'Hazard Ratio':
                        self.fill_input_field('hazardRateNull', row_data, 'Hazard_Rate_Control', 'Enter The value in hazardRateNull Field ')
                        self.fill_input_field('hazardRateAlter', row_data, 'Hazard_Rate_Treatment', 'Enter The value in hazardRateAlter Field ')

                if (row_data['inputMethod'] == 'Median Survival Times'):
                    self.base.selectByvisibleText("InputMethod", row_data['inputMethod'],UnivWaitFor=3)   
                    
                    if row_data['WhatToCompute'] == 'Hazard Ratio':   
                        self.fill_input_field('medianSurvivalTimeNull', row_data, 'MST_Control', 'Enter The value in medianSurvivalTimeNull Field ')   
                    elif row_data['WhatToCompute'] != 'Hazard Ratio':
                        self.fill_input_field('medianSurvivalTimeNull', row_data, 'MST_Control', 'Enter The value in medianSurvivalTimeNull Field ')  
                        self.fill_input_field('medianSurvivalTimeAlter', row_data, 'MST_Treatment', 'Enter The value in medianSurvivalTimeAlter Field ')
                    
                if (row_data['inputMethod'] == 'Cumulative % Survival'):     
                    self.base.selectByvisibleText("InputMethod", row_data['inputMethod']) 
                    
                    if row_data['WhatToCompute'] == 'Hazard Ratio':          
                        self.fill_input_field('byTime', row_data, 'CumPercSurv_ByTime', 'Enter The value in byTime Field ')
                        self.fill_input_field('cumulativeSurvivalNull', row_data, 'CumPercSurv_Control', 'Enter The value in CumPercSurv_Control Field ')                                       
                    elif row_data['WhatToCompute'] != 'Hazard Ratio':
                        self.fill_input_field('byTime', row_data, 'CumPercSurv_ByTime', 'Enter The value in byTime Field ')
                        self.fill_input_field('cumulativeSurvivalNull', row_data, 'CumPercSurv_Control', 'Enter The value in CumPercSurv_Control Field ')                                       
                        self.fill_input_field('cumulativeSurvivalAlter', row_data, 'CumPercSurv_Treatment', 'Enter The value in CumPercSurv_Treatment Field ')                                       
                
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in selecting input method{e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_generic_to_EventCalMethod_SingleArmTTE(self, row_data):
        try:    
            if (row_data['Test']=='Parametric Weibull Distribution' or row_data['Test']=='Logrank Weibull Distribution'):
                self.fill_input_field('weibullShapeParam', row_data, 'Shape', 'Enter The value in Shape Field ')

            if (row_data['Test']=='Logrank Exponential Distribution'):
                if (row_data['EventCalculationMethod']=='Lachin and Foulkes'):
                    self.base.selectByvisibleText("eventCalculationMethod", "Lachin and Foulkes",UnivWaitFor=4)
                elif (row_data['EventCalculationMethod']=='Lawless'):
                    self.base.selectByvisibleText("eventCalculationMethod", "Lawless",UnivWaitFor=4)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering geenric data {e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_SingleArmTTE(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            # TestType = row_data['TestType']
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
            self.process_input_row_generic_SingleArm(row_data,WhatToCompute)            
            # if (row_data['Hypothesis'] == 'Superiority'): 
            self.process_input_row_SingleArmTTE_Inputmethod(row_data)   
            time.sleep(3)
            self.process_input_row_generic_to_EventCalMethod_SingleArmTTE(row_data)   
            time.sleep(3)
            self.process_input_row_enrollment_SingleArm(row_data) 
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in SingleArm TTE{e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_SingleProportion(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            TestType = row_data['TestType']
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
            self.process_input_row_generic(row_data,WhatToCompute)            
            if (row_data['Hypothesis'] == 'Superiority'):                                 
                self.fill_input_field('propResponseUnderNull', row_data, 'propResponseUnderNull', 'Enter The value in propResponseUnderNull Under Null Field ')
                self.fill_input_field('propResponseUnderAlt', row_data, 'propResponseUnderAlt', 'Enter The value in propResponseUnderAlt under Alternative Field ')                
                # self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')
                if (TestType == '2-Sided (Asymmetric)'):
                    self.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
                    self.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field')
                time.sleep(2)                

            self.process_input_row_Assurance(row_data)

            self.process_input_row_enrollement(row_data) 

        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for Single Mean{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_Simon_Two_Stage(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            
            TestType = row_data['TestType']
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])           
            if (row_data['Hypothesis'] == 'Minimax' or row_data['Hypothesis'] == 'Optimal'):                                 
                self.fill_input_field('propResponseUnderNull', row_data, 'propResponseUnderNull', 'Enter The value in propResponseUnderNull Under Null Field ')
                self.fill_input_field('propResponseUnderAlt', row_data, 'propResponseUnderAlt', 'Enter The value in propResponseUnderAlt under Alternative Field ')                
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                time.sleep(2)  
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for Single Mean{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_Assurance(self, row_data):
        try:
            if (str(int(row_data['compAssurance'])) == '1'):
                self.base.click("IncludeAssurance",UnivWaitFor=2)
                self.LogScreenshot.fLogScreenshot(message=f"Clicked on Assurance toggle", pass_=True, log=True, screenshot=True)
                self.base.selectByvisibleText("DistributionMethodDD", row_data['Assurance_distribution'])   
                if (row_data['Assurance_distribution'] == 'Normal' and row_data['Assurance_inputMethod'] == 'Percentiles of μ'):
                    # sign1 
                    # sign2 
                    # Mu_p1Val  
                    # Mu_p2Val  
                    # Mu_prob1  
                    # Mu_prob2
                    self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'])
                    self.base.selectByvisibleText("percMu1stOperator", row_data['sign1'])
                    self.base.selectByvisibleText("percMu2ndOperator", row_data['sign2'])
                    self.fill_input_field('percMu1stPercentileVal', row_data, 'p1Val', 'Enter The value in 1stPercentileVal Field :')
                    self.fill_input_field('percMu2ndPercentileVal', row_data, 'p2Val', 'Enter The value in 2ndPercentileVal Field :')
                    self.fill_input_field('percMu1stPercentileProb', row_data, 'prob1', 'Enter The value in 1stPercentileProb Field :')
                    self.fill_input_field('percMu2ndPercentileProb', row_data, 'prob2', 'Enter The value in 2ndPercentileProb Field :')
                elif (row_data['Assurance_distribution'] == 'Normal' and row_data['Assurance_inputMethod'] == 'E(μ) and SD(μ)'):
                    # e(mu) 
                    # sd(mu)
                    self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'])
                    self.fill_input_field('eMu', row_data, 'E(μ)', 'Enter The value in e(Mu) Field :')
                    self.fill_input_field('sdMu', row_data, 'SD(μ)', 'Enter The value in sd(Mu) Field :')
                    print()
                elif (row_data['Assurance_distribution'] == 'Uniform'):
                    # Pi_min
                    # Pi_max
                    self.fill_input_field('UniformMinTB', row_data, 'min', 'Enter The value in min Field :')
                    self.fill_input_field('UniformMaxTB', row_data, 'max', 'Enter The value in max Field :')
                else:
                    print(f"Different Assurance distribution found")    
                self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided'", pass_=True, log=True, screenshot=True)
                
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for Single Mean{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_Fishers_Extract(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            Prop_InputMethod = row_data['Prop_InputMethod']
            # self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
            self.fill_input_field('AllocationRatioTB', row_data, 'AllocationRatio', 'Enter The value in Allocation Ratio Field :')  
            self.fill_input_field('proportionControl', row_data, 'proportionControl', 'Enter The value in proportionControl under Alternative Field ')                
       
            if WhatToCompute == 'Sample Size':
                self.base.click("Type1ErrorRB", UnivWaitFor=1)
                self.base.click("SampleSizeRB", UnivWaitFor=1)                
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')
                self.fill_input_field('PowerTB', row_data, 'input_power', 'Enter The value in Power Field :')  

            elif WhatToCompute == 'Power':
                self.base.click("PowerRB", UnivWaitFor=1)
                self.fill_input_field_nonfloat('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in SampleSize Field')
                self.fill_input_field('Type1ErrorTB', row_data, 'input_typeIError', 'Enter The value in type1error Field')                                
                                    
            self.fill_input_field('ProbabilityofdropoutTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')
            
            if (Prop_InputMethod == 'User Specified)'):
                self.fill_input_field('proportionTreatment', row_data, 'proportionTreatment', 'Enter The value in proportionTreatment Field')
                time.sleep(2)                
            elif (Prop_InputMethod == 'Odds Ratio'):
                self.fill_input_field('oddsRatio', row_data, 'oddsRatio', 'Enter The value in oddsRatio Field')

            elif (Prop_InputMethod == 'Difference'):
                self.fill_input_field('differenceOfProportions', row_data, 'differenceOfProportions', 'Enter The value in differenceOfProportions Field')

            elif (Prop_InputMethod == 'Ratio'):
                self.fill_input_field('ratioOfProportions', row_data, 'ratioOfProportions', 'Enter The value in ratioOfProportions Field')

            self.process_input_row_enrollement(row_data) 

        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for Fishers Extract'{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_SingleMean(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            TestType = row_data['TestType']
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
            self.process_input_row_generic(row_data,WhatToCompute)            
            if (row_data['Hypothesis'] == 'Superiority'):                                 
                self.fill_input_field('MeanResponseNullTB', row_data, 'meanResponseNull', 'Enter The value in Mean Response Under Null Field ')
                self.fill_input_field('MeanResponseAltTB', row_data, 'meanResponseAlt', 'Enter The value in Mean Response under Alternative Field ')                
                self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')
                if (TestType == '2-Sided (Asymmetric)'):
                    self.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
                    self.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field')
                time.sleep(2)            
            if (str(int(row_data['compAssurance'])) == '1'):
                self.base.click("IncludeAssurance",UnivWaitFor=2)
                self.LogScreenshot.fLogScreenshot(message=f"Clicked on Assurance toggle", pass_=True, log=True, screenshot=True)
                self.base.selectByvisibleText("DistributionMethodDD", row_data['Assurance_distribution'])   
                if (row_data['Assurance_distribution'] == 'Normal' and row_data['Assurance_inputMethod'] == 'Percentiles of μ'):
                    # sign1 
                    # sign2 
                    # Mu_p1Val  
                    # Mu_p2Val  
                    # Mu_prob1  
                    # Mu_prob2
                    self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'])
                    self.base.selectByvisibleText("percMu1stOperator", row_data['sign1'])
                    self.base.selectByvisibleText("percMu2ndOperator", row_data['sign2'])
                    self.fill_input_field('percMu1stPercentileVal', row_data, 'p1Val', 'Enter The value in 1stPercentileVal Field :')
                    self.fill_input_field('percMu2ndPercentileVal', row_data, 'p2Val', 'Enter The value in 2ndPercentileVal Field :')
                    self.fill_input_field('percMu1stPercentileProb', row_data, 'prob1', 'Enter The value in 1stPercentileProb Field :')
                    self.fill_input_field('percMu2ndPercentileProb', row_data, 'prob2', 'Enter The value in 2ndPercentileProb Field :')
                elif (row_data['Assurance_distribution'] == 'Normal' and row_data['Assurance_inputMethod'] == 'E(μ) and SD(μ)'):
                    # e(mu) 
                    # sd(mu)
                    self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'])
                    self.fill_input_field('eMu', row_data, 'E(μ)', 'Enter The value in e(Mu) Field :')
                    self.fill_input_field('sdMu', row_data, 'SD(μ)', 'Enter The value in sd(Mu) Field :')
                    print()
                elif (row_data['Assurance_distribution'] == 'Uniform'):
                    # Pi_min
                    # Pi_max
                    self.fill_input_field('UniformMinTB', row_data, 'min', 'Enter The value in min Field :')
                    self.fill_input_field('UniformMaxTB', row_data, 'max', 'Enter The value in max Field :')
                else:
                    print(f"Different Assurance distribution found")    
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided'", pass_=True, log=True, screenshot=True)
            self.process_input_row_enrollement(row_data)            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for Single Mean{e}", pass_=False, log=True, screenshot=True)

    def process_input_row_DOM(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            TestType = row_data['TestType']
            
            self.process_input_row_generic(row_data, WhatToCompute)        
            self.fill_input_field('AllocationRatioTB', row_data, 'AllocationRatio', 'Enter The value in Allocation Ratio Field :')  

            InputMethod = row_data['InputMethod']              
            self.base.selectByvisibleText("InputMethod", row_data['InputMethod'])
            self.base.selectByvisibleText("TestStatisticDD", row_data['TestStatistic'])                  
            
            if InputMethod == 'Difference of Means' and WhatToCompute != 'Diff. in Means' and (row_data['Hypothesis'] == 'Superiority'):
                self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
                self.fill_input_field('DifferenceofMeansTB', row_data, 'input_diffInMeans', 'Enter The value in Difference of Means Field ')
                self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
                if (TestType == '2-Sided (Asymmetric)'):
                    self.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
                    self.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field')                
            
            elif InputMethod == 'Individual Means' and WhatToCompute != 'Diff. in Means' and (row_data['Hypothesis'] == 'Superiority'):
                self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
                self.fill_input_field('MeanControlTB', row_data, 'meanCtrl', 'Enter The value in Mean control Field ')
                self.fill_input_field('MeanTreatmentTB', row_data, 'meanTrmt', 'Enter The value in Mean Treatment Field ')             
                self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
            
            elif InputMethod == 'Standardized Diff. of Means' and WhatToCompute != 'Diff. in Means' and (row_data['Hypothesis'] == 'Superiority'):
                self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
                self.fill_input_field('standardizedDifferenceTB', row_data, 'stdDiffInMeans', 'Enter The value in stdDiffInMeans Field ')

            if (row_data['Hypothesis'] == 'Super Superiority' ) :
                if InputMethod == 'Individual Means':
                        self.fill_input_field('SuperSuperiority_MeanControl', row_data, 'meanCtrl', 'Enter The value in Mean control Field ')
                        self.fill_input_field('SuperSuperiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                        self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
                        self.fill_input_field('supsup_differenceInMeans', row_data, 'input_diffInMeans', 'Enter The value in supsup_differenceInMeans Field :')
                elif InputMethod == "Difference of Means" :
                    if WhatToCompute != 'Diff. in Means':
                        self.fill_input_field('SuperSuperiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                        self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
                        self.fill_input_field('supsup_differenceInMeans', row_data, 'input_diffInMeans', 'Enter The value in supsup_differenceInMeans Field :')
                    else:
                        self.fill_input_field('SuperSuperiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                        self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
            if (row_data['Hypothesis'] == 'Noninferiority'):
                if InputMethod == 'Individual Means':
                    self.fill_input_field('Noninferiority_MeanControl', row_data, 'meanCtrl', 'Enter The value in Mean control Field ')    
                    self.fill_input_field('Noninferiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                    self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
                    self.fill_input_field('nonInf_differenceInMeans', row_data, 'input_diffInMeans', 'Enter The value in nonInf_differenceInMeans Field :')
                elif InputMethod == "Difference of Means" and WhatToCompute != 'Diff. in Means':
                    self.fill_input_field('Noninferiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                    self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')
                    self.fill_input_field('nonInf_differenceInMeans', row_data, 'input_diffInMeans', 'Enter The value in nonInf_differenceInMeans Field :')
                elif InputMethod == "Difference of Means" and WhatToCompute == 'Diff. in Means':
                    self.fill_input_field('Noninferiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')    
                    self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in standard dev Field :')

            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided",
                                        pass_=True, log=True, screenshot=True)
            if (str(int(row_data['compAssurance'])) == '1'):
                # Calling the common assurance input method for DOM & MOPD
                self.process_DOM_MOPD_Assurance(row_data)

            if (str(int(row_data['includeAccrualDropout']))== '1'):
                self.base.click("Enrollment_leftpanellink",UnivWaitFor = 4)
                self.process_input_row_enrollement(row_data)  

        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for {e}", pass_=False, log=True, screenshot=True)

    def process_input_row_DOP_ROP(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            TestType = row_data['TestType'] 
            self.fill_input_field('AllocationRatioTB', row_data, 'AllocationRatio', 'Enter The value in Allocation Ratio Field :')  
            self.process_input_row_generic(row_data, WhatToCompute)  
            
            if (row_data['Hypothesis'] == 'Superiority'):
                self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])                
                # self.fill_input_field('proportionUnderControl_SP', row_data, 'propCtrl', 'Enter The value in propCtrl Field ')
                # self.base.selectByvisibleText("variance", row_data['variance'])  

                '''Conditions for Difference Of Proportion'''
                if (row_data['Test'] == 'Difference of Proportions'):
                    self.fill_input_field('proportionUnderControl_SP', row_data, 'propCtrl', 'Enter The value in propCtrl Field ')
                    self.base.selectByvisibleText("variance", row_data['variance'])  
                    self.fill_input_field('differenceInProportions_SP', row_data, 'diffInProp', 'Enter The value in diffInProp Field ')   
                    if (str(int(row_data['usePikeSmithCorrection'])) == '1'):
                        self.base.click("usePikeSmithCorrection",UnivWaitFor=1) 
                        time.sleep(2) 
                
                '''Conditions for Ratio Of Proportion'''
                if (row_data['Test'] == 'Ratio of Proportions'):
                    self.fill_input_field('ratioOfProportions_SP', row_data, 'ratioInProp', 'Enter The value in ratioOfProportions_SP Field ')                
                    self.base.selectByvisibleText("variance", row_data['variance'])  

                elif (row_data['Test'] == 'Odds Ratio of Proportions'):
                    self.fill_input_field('oddsRatioOfProportions_SP', row_data, 'OddsratioInProp', 'Enter The value in oddsRatioOfProportions_SP Field ')
                    time.sleep(2)                
                                
                                             
                if (TestType == '2-Sided (Asymmetric)'):
                    self.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
                    self.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field') 

            if (row_data['Hypothesis'] == 'Super Superiority'):
                self.fill_input_field('proportionUnderControl_SS', row_data, 'propCtrl', 'Enter The value in propCtrl Field ')
                
                '''Conditions for Ratio Of Proportion'''
                if (row_data['Test'] == 'Ratio of Proportions'):
                    self.fill_input_field('ratioOfProportions_SS', row_data, 'ratioInProp', 'Enter The value in ratioOfProportions_SS Field ')                
                elif (row_data['Test'] == 'Odds Ratio of Proportions'):
                    self.fill_input_field('oddsRatioOfProportions_SS', row_data, 'OddsratioInProp', 'Enter The value in oddsRatioOfProportions_SS Field ')
                else:                               
                    self.fill_input_field('differenceInProportions_SS', row_data, 'diffInProp', 'Enter The value in diffInProp Field :')
                self.fill_input_field('superSuperiorityMargin', row_data, 'margin', 'Enter The value in margin Field :')

            if (row_data['Hypothesis'] == 'Noninferiority'):
                self.fill_input_field('proportionUnderControl_NI', row_data, 'propCtrl', 'Enter The value in propCtrl Field ')            
                
                '''Conditions for Ratio Of Proportion'''
                if (row_data['Test'] == 'Ratio of Proportions'):
                    self.fill_input_field('ratioOfProportions_NI', row_data, 'ratioInProp', 'Enter The value in ratioOfProportions_NI Field ')
                    
                    if(row_data['testStatistic'] == 'Score (Farrington Manning)'):
                        self.base.selectByvisibleText("testStatistic", row_data['testStatistic'])
                        self.base.selectByvisibleText("scoreTestStatisticVariance", row_data['scoreTestStatisticVariance']) 
                    elif (row_data['testStatistic'])=='Wald':
                        self.base.selectByvisibleText("testStatistic", row_data['testStatistic'])

                elif (row_data['Test'] == 'Odds Ratio of Proportions'):
                    self.fill_input_field('oddsRatioOfProportions_NI', row_data, 'OddsratioInProp', 'Enter The value in oddsRatioOfProportions_NI Field ')
                else:                               
                    self.fill_input_field('differenceInProportions_NI', row_data, 'diffInProp', 'Enter The value in diffInProp Field :')
                    if (str(int(row_data['usePikeSmithCorrection'])) == '1'):
                        self.base.click("usePikeSmithCorrection",UnivWaitFor=1)
                self.fill_input_field('nonInferiorityMargin', row_data, 'margin', 'Enter The value in margin Field :')                
            
            if (str(int(row_data['compAssurance'])) == '1'):
                self.base.click("IncludeAssurance",UnivWaitFor=1)
                self.base.selectByvisibleText("PriorDistributionForDD", row_data['priorDistributionFor'])
                self.base.selectByvisibleText("DistributionMethodDD", row_data['Assurance_distribution'])                
                if (row_data['Assurance_distribution'] != 'Uniform'):                      
                    self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'])                              
                if (row_data['Assurance_distribution'] == 'Beta') and (row_data['priorDistributionFor'] == 'Π_c and Π_t'):
                    if (row_data['Assurance_inputMethod'] == 'Percentiles of Π_c and Π_t'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        # sign1_2(forPercOf_cAndt)	
                        # sign2_2(forPercOf_cAndt)	
                        # Pi_p1Val_2(forPercOf_cAndt)	
                        # Pi_p2Val_2(forPercOf_cAndt)	
                        # Pi_prob1_2(forPercOf_cAndt)	
                        # Pi_prob2_2(forPercOf_cAndt)
                        self.base.selectByvisibleText("percPiC1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiC2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiC1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiC1stPercentileVal Field :')
                        self.fill_input_field('percPiC2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiC2ndPercentileVal Field :')
                        self.fill_input_field('percPiC1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiC1stPercentileProb Field :')
                        self.fill_input_field('percPiC2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiC2ndPercentileProb Field :')

                        self.base.selectByvisibleText("percPiT1stOperator", row_data['sign1_2(forPercOf_cAndt)'])
                        self.base.selectByvisibleText("percPiT2ndOperator", row_data['sign2_2(forPercOf_cAndt)'])
                        self.fill_input_field('percPiT1stPercentileVal', row_data, 'Pi_p1Val_2(forPercOf_cAndt)', 'Enter The value in percPiC1stPercentileVal Field :')
                        self.fill_input_field('percPiT2ndPercentileVal', row_data, 'Pi_p2Val_2(forPercOf_cAndt)', 'Enter The value in percPiC2ndPercentileVal Field :')
                        self.fill_input_field('percPiT1stPercentileProb', row_data, 'Pi_prob1_2(forPercOf_cAndt)', 'Enter The value in percPiC1stPercentileProb Field :')
                        self.fill_input_field('percPiT2ndPercentileProb', row_data, 'Pi_prob2_2(forPercOf_cAndt)', 'Enter The value in percPiC2ndPercentileProb Field :')
                        print()
                    elif (row_data['Assurance_inputMethod'] == 'Beta Parameters (a and b)'):
                        # piParams_a	
                        # piParams_b
                        # piParams_a_2(forPercOf_cAndt)	
                        # piParams_b_2(forPercOf_cAndt)
                        self.fill_input_field('pi_c_a', row_data, 'piParams_a', 'Enter The value in pi_c_a Field :')
                        self.fill_input_field('pi_c_b', row_data, 'piParams_b', 'Enter The value in pi_c_b Field :')
                        self.fill_input_field('pi_t_a', row_data, 'piParams_a', 'Enter The value in pi_t_a Field :')
                        self.fill_input_field('pi_t_b', row_data, 'piParams_b', 'Enter The value in pi_t_b Field :')
                        print()
                if (row_data['Assurance_distribution'] == 'Beta') and (row_data['priorDistributionFor'] == 'Π_c'):
                    if (row_data['Assurance_inputMethod'] == 'Beta Parameters (a and b)'):
                        # piParams_a	
                        # piParams_b
                        self.fill_input_field('pi_c_a', row_data, 'piParams_a', 'Enter The value in pi_c_a Field :')
                        self.fill_input_field('pi_c_b', row_data, 'piParams_b', 'Enter The value in pi_c_b Field :')
                        
                    elif (row_data['Assurance_inputMethod'] == 'Percentiles of Π_c'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiC1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiC2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiC1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiC1stPercentileVal Field :')
                        self.fill_input_field('percPiC2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiC2ndPercentileVal Field :')
                        self.fill_input_field('percPiC1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiC1stPercentileProb Field :')
                        self.fill_input_field('percPiC2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiC2ndPercentileProb Field :')
                        
                    elif (row_data['Assurance_inputMethod'] == 'Percentiles of δ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiCDelta1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiCDelta2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiCDelta1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiCDelta1stPercentileVal Field :')
                        self.fill_input_field('percPiCDelta2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiCDelta2ndPercentileVal Field :')
                        self.fill_input_field('percPiCDelta1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiCDelta1stPercentileProb Field :')
                        self.fill_input_field('percPiCDelta2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiCDelta2ndPercentileProb Field :')
                    
                    elif (row_data['Assurance_inputMethod'] == 'Percentiles of ρ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiCRho1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiCRho2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiCRho1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiCRho1stPercentileVal Field :')
                        self.fill_input_field('percPiCRho2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiCRho2ndPercentileVal Field :')
                        self.fill_input_field('percPiCRho1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiCRho1stPercentileProb Field :')
                        self.fill_input_field('percPiCRho2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiCRho2ndPercentileProb Field :')    
                    elif (row_data['Assurance_inputMethod'] == 'Percentiles of Ψ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiCPsi1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiCPsi2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiCPsi1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiCPsi1stPercentileVal Field :')
                        self.fill_input_field('percPiCPsi2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiCPsi2ndPercentileVal Field :')
                        self.fill_input_field('percPiCPsi1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiCPsi1stPercentileProb Field :')
                        self.fill_input_field('percPiCPsi2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiCPsi2ndPercentileProb Field :')    
                
                if (row_data['Assurance_distribution'] == 'Beta') and (row_data['priorDistributionFor'] == 'Π_t'):
                    if (row_data['Assurance_inputMethod'] == 'Beta Parameters (a and b)'):
                        # piParams_a	
                        # piParams_b
                        self.fill_input_field('pi_t_a', row_data, 'piParams_a', 'Enter The value in pi_t_a Field :')
                        self.fill_input_field('pi_t_b', row_data, 'piParams_b', 'Enter The value in pi_t_b Field :')
                        
                    if (row_data['Assurance_inputMethod'] == 'Percentiles of Π_t'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiT1stOperator", row_data['sign1_2(forPercOf_cAndt)'])
                        self.base.selectByvisibleText("percPiT2ndOperator", row_data['sign2_2(forPercOf_cAndt)'])
                        self.fill_input_field('percPiT1stPercentileVal', row_data, 'Pi_p1Val_2(forPercOf_cAndt)', 'Enter The value in percPiC1stPercentileVal Field :')
                        self.fill_input_field('percPiT2ndPercentileVal', row_data, 'Pi_p2Val_2(forPercOf_cAndt)', 'Enter The value in percPiC2ndPercentileVal Field :')
                        self.fill_input_field('percPiT1stPercentileProb', row_data, 'Pi_prob1_2(forPercOf_cAndt)', 'Enter The value in percPiC1stPercentileProb Field :')
                        self.fill_input_field('percPiT2ndPercentileProb', row_data, 'Pi_prob2_2(forPercOf_cAndt)', 'Enter The value in percPiC2ndPercentileProb Field :')
                        
                    if (row_data['Assurance_inputMethod'] == 'Percentiles of δ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiTDelta1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiTDelta2ndOperator", row_data['sign2'])
                        self.fill_input_field('percPiTDelta1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiTDelta1stPercentileVal Field :')
                        self.fill_input_field('percPiTDelta2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiTDelta2ndPercentileVal Field :')
                        self.fill_input_field('percPiTDelta1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiTDelta1stPercentileProb Field :')
                        self.fill_input_field('percPiTDelta2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiTDelta2ndPercentileProb Field :')
                    
                    if (row_data['Assurance_inputMethod'] == 'Percentiles of ρ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiTRho1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiTRho2ndOperator", row_data['sign2'])
                        time.sleep(5)
                        self.fill_input_field('percPiTRho1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiTRho1stPercentileVal Field :')
                        self.fill_input_field('percPiTRho2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiTRho2ndPercentileVal Field :')
                        self.fill_input_field('percPiTRho1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiTRho1stPercentileProb Field :')
                        self.fill_input_field('percPiTRho2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiTRho2ndPercentileProb Field :')        
                    if (row_data['Assurance_inputMethod'] == 'Percentiles of Ψ'):
                        # sign1	
                        # sign2	
                        # Pi_p1Val	
                        # Pi_p2Val	
                        # Pi_prob1	
                        # Pi_prob2
                        self.base.selectByvisibleText("percPiTPsi1stOperator", row_data['sign1'])
                        self.base.selectByvisibleText("percPiTPsi2ndOperator", row_data['sign2'])
                        time.sleep(5)
                        self.fill_input_field('percPiTPsi1stPercentileVal', row_data, 'Pi_p1Val', 'Enter The value in percPiTPsi1stPercentileVal Field :')
                        self.fill_input_field('percPiTPsi2ndPercentileVal', row_data, 'Pi_p2Val', 'Enter The value in percPiTPsi2ndPercentileVal Field :')
                        self.fill_input_field('percPiTPsi1stPercentileProb', row_data, 'Pi_prob1', 'Enter The value in percPiTPsi1stPercentileProb Field :')
                        self.fill_input_field('percPiTPsi2ndPercentileProb', row_data, 'Pi_prob2', 'Enter The value in percPiTPsi2ndPercentileProb Field :')        
                
                if (row_data['Assurance_distribution'] == 'Uniform') and (row_data['priorDistributionFor'] == 'Π_c'):
                    # Pi_min
                    # Pi_max
                    print("(((((((((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))))))")
                    self.fill_input_field('minPiC', row_data, 'Pi_min', 'Enter The value in minPiC Field :')
                    self.fill_input_field('maxPiC', row_data, 'Pi_max', 'Enter The value in maxPiC Field :')                    
                if (row_data['Assurance_distribution'] == 'Uniform') and (row_data['priorDistributionFor'] == 'Π_t'):
                    # Pi_min
                    # Pi_max
                    self.fill_input_field('minPiT', row_data, 'Pi_min', 'Enter The value in minPiC Field :')
                    self.fill_input_field('maxPiT', row_data, 'Pi_max', 'Enter The value in maxPiC Field :')                    
                if (row_data['Assurance_distribution'] == 'Uniform') and (row_data['priorDistributionFor'] == 'Π_c and Π_t'):
                    # Pi_min
                    # Pi_max
                    # Pi_min_2(forPercOf_cAndt)	
                    # Pi_max_2(forPercOf_cAndt)
                    self.fill_input_field('minPiC', row_data, 'Pi_min', 'Enter The value in minPiC Field :')
                    self.fill_input_field('maxPiC', row_data, 'Pi_max', 'Enter The value in maxPiC Field :')
                    self.fill_input_field('minPiT', row_data, 'Pi_min_2(forPercOf_cAndt)', 'Enter The value in minPiT Field :')
                    self.fill_input_field('maxPiT', row_data, 'Pi_max_2(forPercOf_cAndt)', 'Enter The value in maxPiT Field :')                    
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided'", pass_=True, log=True, screenshot=True)
            self.process_input_row_enrollement(row_data)            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for {e}", pass_=False, log=True, screenshot=True)

    def fill_input_field(self, field_name, row_data, column_name, log_message):
        """
        Fill an input field using data from the specified column in the row_data Series.

        Parameters:
            field_name (str): Name of the input field in the application.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            column_name (str): Name of the column in datafile to retrieve the input value from.
            log_message (str): Log message for successful input operation.
        """
        try:
            # Get the value from the row data
            input_value = row_data[column_name]

            # Check if the column name is 'input_sampleSize'
            if column_name == 'input_sampleSize':
                # Attempt to convert the value to a string without decimals
                try:
                    input_value = str(int(float(input_value)))
                except ValueError:
                    # Handle the case where the conversion to float/int fails
                    input_value = str(input_value)
            else:
                # For other columns, just convert the value to string
                input_value = str(input_value)

            # Input the value into the field
            self.base.input_text_with_ctrlAltDel(field_name, input_value, UnivWaitFor=1)

            self.LogScreenshot.fLogScreenshot(message=log_message, pass_=True, log=True, screenshot=True)
            
        except Exception as e:
            # Log failure
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering {e}", pass_=False, log=True, screenshot=True)

    def fill_input_field_nonfloat(self, field_name, row_data, column_name, log_message):
        """
        Fill an input field using data from the specified column in the row_data Series.

        Parameters:
            field_name (str): Name of the input field in the application.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            column_name (str): Name of the column in datafile to retrieve the input value from.
            log_message (str): Log message for successful input operation.
        """
        try:
            # Use the value as is for other columns
            # input_value = str(row_data[column_name])
                input_value = (row_data[column_name]) 
                input_value = str(int(float(input_value)))   
                self.base.input_text_with_ctrlAltDel(field_name, input_value, UnivWaitFor=1)
                self.LogScreenshot.fLogScreenshot(message=log_message, pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering {e}", pass_=False, log=True, screenshot=True)

    def generate_results_and_navigate_to_page(self, index,LogScreenshot):
        """
        Generate results and navigate to the results page.

        Parameters:
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
        """
        try:
            # Click on the corresponding result set based on the iteration index
            # self.base.click("ResultsPage", UnivWaitFor=10)
            
            result_set_xpath = f"//a[contains(text(),'Result - Input Set {index}')]"
            print(result_set_xpath)
            count = len(result_set_xpath)
            # result_set_xpath="//a[contains(text(),'Result - Input Set {}')]".format(index)
            print("result name:", count)
            self.driver.find_element(By.XPATH, result_set_xpath).click()
            # # for i in range(1, ResultSetCount + 1):
            # print("Results-", index, "clicked")    
            # self.driver.find_element(By.XPATH, result_set_xpath).click()
            # self.LogScreenshot.fLogScreenshot(message="detailed Results screen", pass_=True, log=True, screenshot=True)
            # self.base.click(result_set_xpath, UnivWaitFor=10)

            # Log the navigation to the results page
            self.LogScreenshot.fLogScreenshot(message=f"Clicked on 'Result - Input Set {index + 1}' and landed on Results page",
                                        pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error navigating to Results page: {e}", pass_=False, log=True, screenshot=True)

    def check_if_is_number(self, value):
        # Check if the value is a number (integer or float) and does not contain alphabetic characters
        return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None
    
    def assert_passforSciChars(self, expected, actual):
        # Define a mapping of acceptable variations
        acceptable_variations = {
            'Percentiles of Π_c': 'Percentiles of PiC',
            'Percentiles of Π_t': 'Percentiles of PiT',
            'Percentiles of δ': 'Percentiles of Delta',
            'Percentiles of Π_c and Π_t': 'Percentiles of PiC and PiT',
            'Π_c and Π_t' : 'PiC and PiT',
            'Π_c' : 'PiC',
            'Π_t' : 'PiT',
            'δ' : 'Delta',
            'E(δ) and SD(δ)' : 'E and SD of Delta',
            'Percentiles of δ/σ' : 'Percentiles of Delta by Sigma',
            'Percentiles of ρ' : 'Percentiles of Rho',
            'Percentiles of Ψ':'Percentiles of Psi',
            'Percentiles of μ':'Percentiles of Mu',
            'E(μ) and SD(μ)':'E and SD of Mu'
        }        
        # Check if the actual value is an acceptable variation of the expected value
        if acceptable_variations.get(expected) == actual:
            return "PASS"
        else:
            return "FAIL: Mismatching column 'Assurance_inputMethod': Expected({}), Actual({})".format(expected, actual)

    def validate_results(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        try:
            
            # Retrieve actual results from the results page
            actual_results = self.get_actual_results_from_page()

            # Compare actual results with expected values (row_data)
            matching_columns = []
            mismatching_columns = []

            for column, expected_value in row_data.items():
                actual_value = actual_results.get(column, None)
                
                if actual_value is not None and actual_value != 'N/A' and expected_value != 'nan':
                    result = self.assert_passforSciChars(expected_value, actual_value)
                    print(result)
                    if self.check_if_is_number(actual_value) and self.check_if_is_number(expected_value):
                        actual_value = round(float(actual_value), 3)
                        expected_value = round(float(expected_value), 3)
                    else:
                        actual_value = str(actual_value)
                        expected_value = str(expected_value)

                    if str(actual_value) == str(expected_value) or result == "PASS":
                        matching_columns.append((column, expected_value, actual_value))
                        tc_status.append("PASS")
                    else:
                        mismatching_columns.append((column, expected_value, actual_value))
                        tc_status.append("FAIL")

            self.LogScreenshot.fLogScreenshot(message=f"Results page", pass_=True, log=True, screenshot=True)
            time.sleep(2)  # Wait for 1 second to load new content 
            
            # self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[3]')
            # time.sleep(2)  # Wait for 1 second to load new content 
            # self.LogScreenshot.fLogScreenshot(message=f"Results page - Part 2", pass_=True, log=True, screenshot=True)

            # Log mismatching columns and their values
            if matching_columns:
                for column, expected, actual in matching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Matching column '{column}': Expected({expected}), Actual({actual})",                                                
                                            pass_=True, log=True, screenshot=False)
            
            # Log mismatching columns and their values
            if mismatching_columns:
                for column, expected, actual in mismatching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                                pass_=False, log=True, screenshot=False)            

        except Exception as e:
            LogScreenshot.fLogScreenshot(
                message=f"Error in results validation: {e}",
                pass_=False, log=True, screenshot=True
            )
            tc_status.append("FAIL")

    def get_actual_results_from_page(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}       
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)
            # Assign specific key-value pairs based on column_to_key_mapping
            # actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['StatisticalDesign'] = Webpage_dict.get('StatisticalDesign', 'N/A')
            actual_results['Test'] = Webpage_dict.get('Test', 'N/A')
            actual_results['inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            actual_results['Hypothesis'] = Webpage_dict.get('Hypothesis', 'N/A')
            actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            actual_results['AllocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            actual_results['TestStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            actual_results['stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            actual_results['sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')            
            actual_results['power'] = Webpage_dict.get('Power', 'N/A')
            actual_results['probofSuccess'] = Webpage_dict.get('Probability of Success', 'N/A')        
            actual_results['variance'] = Webpage_dict.get('Variance', 'N/A')
            actual_results['priorDistributionFor'] = Webpage_dict.get('Prior Distribution for', 'N/A')
            actual_results['Assurance_distribution'] = Webpage_dict.get('Distribution Method', 'N/A')        
            actual_results['E(δ)'] = Webpage_dict.get('E(δ)', 'N/A')
            actual_results['SD(δ)'] = Webpage_dict.get('SD(δ)', 'N/A')
            actual_results['piParams_a'] = Webpage_dict.get('a', 'N/A')
            actual_results['piParams_b'] = Webpage_dict.get('b', 'N/A')
            actual_results['propCtrl'] = Webpage_dict.get('Proportion Under Control', 'N/A')
            actual_results['propTrmt'] = Webpage_dict.get('Proportion Under Treatment', 'N/A')
            actual_results['margin'] = Webpage_dict.get('Under H0', 'N/A')
            actual_results['diffInProp'] = Webpage_dict.get('Under H1', 'N/A') 
                   
            actual_results['maxInfo'] = Webpage_dict.get('Information', 'N/A')
            actual_results['completers'] = Webpage_dict.get('Completers:', 'N/A')
            actual_results['accrualDuration'] = Webpage_dict.get('Accrual Duration', 'N/A')
            actual_results['studyDuration'] = Webpage_dict.get('Study Duration', 'N/A')
            actual_results['criticalPt'] = Webpage_dict.get('Critical Point', 'N/A')
            actual_results['diffInMeans'] = Webpage_dict.get('Under H1', 'N/A')   
            actual_results['ratioOfMeans'] = Webpage_dict.get('Under H1', 'N/A')  
            actual_results['meanRespNull'] = Webpage_dict.get('Mean Response under Null', 'N/A')
            actual_results['meanRespAlt'] = Webpage_dict.get('Mean Response under Alternative', 'N/A') 

            # actual_results['Assurance_inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            # actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A') for DOM this column value going for droupctrl
            # actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')for DOM this column value going for drouptrtmnt
            # actual_results['dropoutsCtrl'] = Webpage_dict.get('Mean Control', 'N/A') Repeated column-DOM
            # actual_results['dropoutsTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')Repeated column-DOM
            # actual_results['sampleSizeTrmt'] = Webpage_dict.get('Treatment', 'N/A')
            # actual_results['sampleSizeCtrl'] = Webpage_dict.get('Control', 'N/A') 
            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results

    def validate_results_SingleSurvival(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        try:
            
            # Retrieve actual results from the results page
            actual_results = self.get_actual_results_from_page_SingleSurvival()

            # Compare actual results with expected values (row_data)
            matching_columns = []
            mismatching_columns = []

            for column, expected_value in row_data.items():
                actual_value = actual_results.get(column, None)
                
                if actual_value is not None and actual_value != 'N/A' and expected_value != 'nan':
                    result = self.assert_passforSciChars(expected_value, actual_value)
                    print(result)
                    if self.check_if_is_number(actual_value) and self.check_if_is_number(expected_value):
                        actual_value = round(float(actual_value), 3)
                        expected_value = round(float(expected_value), 3)
                    else:
                        actual_value = str(actual_value)
                        expected_value = str(expected_value)

                    if str(actual_value) == str(expected_value) or result == "PASS":
                        matching_columns.append((column, expected_value, actual_value))
                        tc_status.append("PASS")
                    else:
                        mismatching_columns.append((column, expected_value, actual_value))
                        tc_status.append("FAIL")

            self.LogScreenshot.fLogScreenshot(message=f"Results page", pass_=True, log=True, screenshot=True)
            time.sleep(2)  # Wait for 1 second to load new content 
            
            # self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[3]')
            # time.sleep(2)  # Wait for 1 second to load new content 
            # self.LogScreenshot.fLogScreenshot(message=f"Results page - Part 2", pass_=True, log=True, screenshot=True)

            # Log mismatching columns and their values
            if matching_columns:
                for column, expected, actual in matching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Matching column '{column}': Expected({expected}), Actual({actual})",                                                
                                            pass_=True, log=True, screenshot=False)
            
            # Log mismatching columns and their values
            if mismatching_columns:
                for column, expected, actual in mismatching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                                pass_=False, log=True, screenshot=False)            

        except Exception as e:
            LogScreenshot.fLogScreenshot(
                message=f"Error in results validation: {e}",
                pass_=False, log=True, screenshot=True
            )
            tc_status.append("FAIL")

    def get_actual_results_from_page_SingleSurvival(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}       
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)
            # Assign specific key-value pairs based on column_to_key_mapping
            # actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['StatisticalDesign'] = Webpage_dict.get('StatisticalDesign', 'N/A')
            actual_results['Test'] = Webpage_dict.get('Test', 'N/A')
            actual_results['inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            actual_results['Hypothesis'] = Webpage_dict.get('Hypothesis', 'N/A')
            actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            actual_results['AllocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            actual_results['TestStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            actual_results['stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            actual_results['sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')            
            actual_results['power'] = Webpage_dict.get('Power', 'N/A')
            actual_results['probofSuccess'] = Webpage_dict.get('Probability of Success', 'N/A')        
            actual_results['variance'] = Webpage_dict.get('Variance', 'N/A')
            actual_results['priorDistributionFor'] = Webpage_dict.get('Prior Distribution for', 'N/A')
            actual_results['Assurance_distribution'] = Webpage_dict.get('Distribution Method', 'N/A')        
            actual_results['E(δ)'] = Webpage_dict.get('E(δ)', 'N/A')
            actual_results['SD(δ)'] = Webpage_dict.get('SD(δ)', 'N/A')
            actual_results['piParams_a'] = Webpage_dict.get('a', 'N/A')
            actual_results['piParams_b'] = Webpage_dict.get('b', 'N/A')
            actual_results['propCtrl'] = Webpage_dict.get('Proportion Under Control', 'N/A')
            actual_results['propTrmt'] = Webpage_dict.get('Proportion Under Treatment', 'N/A')
            actual_results['margin'] = Webpage_dict.get('Under H0', 'N/A')
            actual_results['diffInProp'] = Webpage_dict.get('Under H1', 'N/A') 
            actual_results['EventCalculationMethod'] = Webpage_dict.get('Event Calculation Method', 'N/A') 
            actual_results['MST_Control'] = Webpage_dict.get('Median survival time under Null', 'N/A') 
            actual_results['MST_Treatment'] = Webpage_dict.get('Median survival time under ALternative', 'N/A') 
            actual_results['ExponentialDropoutRate'] = Webpage_dict.get('Dropout Hazard Rate', 'N/A') 
            actual_results['Hazard_Rate_Control'] = Webpage_dict.get('Hazard Rate under Null', 'N/A') 
            actual_results['Hazard_Rate_Treatment'] = Webpage_dict.get('Hazard Rate under Alternative', 'N/A') 
            actual_results['HazardRatio'] = Webpage_dict.get('Hazard Ratio', 'N/A') 
            actual_results['CumPercSurv_ByTime'] = Webpage_dict.get('By Time', 'N/A') 
            actual_results['CumPercSurv_Control'] = Webpage_dict.get('Cumulative % Survival under Null', 'N/A') 
            actual_results['CumPercSurv_Treatment'] = Webpage_dict.get('Cumulative % Survival under Alternative', 'N/A') 
            actual_results['Shape'] = Webpage_dict.get('Weibull Shape Parameter', 'N/A') 

             
            actual_results['maxInfo'] = Webpage_dict.get('Information', 'N/A')
            actual_results['completers'] = Webpage_dict.get('Completers:', 'N/A')
            actual_results['accrualDuration'] = Webpage_dict.get('Accrual Duration', 'N/A')
            actual_results['studyDuration'] = Webpage_dict.get('Study Duration', 'N/A')
            actual_results['criticalPt'] = Webpage_dict.get('Critical Point', 'N/A')
            actual_results['diffInMeans'] = Webpage_dict.get('Under H1', 'N/A')   
            actual_results['ratioOfMeans'] = Webpage_dict.get('Under H1', 'N/A')  
            actual_results['meanRespNull'] = Webpage_dict.get('Mean Response under Null', 'N/A')
            actual_results['meanRespAlt'] = Webpage_dict.get('Mean Response under Alternative', 'N/A') 

            # actual_results['Assurance_inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            # actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A') for DOM this column value going for droupctrl
            # actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')for DOM this column value going for drouptrtmnt
            # actual_results['dropoutsCtrl'] = Webpage_dict.get('Mean Control', 'N/A') Repeated column-DOM
            # actual_results['dropoutsTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')Repeated column-DOM
            # actual_results['sampleSizeTrmt'] = Webpage_dict.get('Treatment', 'N/A')
            # actual_results['sampleSizeCtrl'] = Webpage_dict.get('Control', 'N/A') 
            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results

    def validate_results_DOM(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        try:
            
            # Retrieve actual results from the results page
            actual_results = self.get_actual_results_from_page_DOM()

            # Compare actual results with expected values (row_data)
            matching_columns = []
            mismatching_columns = []

            for column, expected_value in row_data.items():
                actual_value = actual_results.get(column, None)
                
                if actual_value is not None and actual_value != 'N/A' and expected_value != 'nan':
                    result = self.assert_passforSciChars(expected_value, actual_value)
                    print(result)
                    if self.check_if_is_number(actual_value) and self.check_if_is_number(expected_value):
                        actual_value = round(float(actual_value), 3)
                        expected_value = round(float(expected_value), 3)
                    else:
                        actual_value = str(actual_value)
                        expected_value = str(expected_value)

                    if str(actual_value) == str(expected_value) or result == "PASS":
                        matching_columns.append((column, expected_value, actual_value))
                        tc_status.append("PASS")
                    else:
                        mismatching_columns.append((column, expected_value, actual_value))
                        tc_status.append("FAIL")

            self.LogScreenshot.fLogScreenshot(message=f"Results page", pass_=True, log=True, screenshot=True)
            time.sleep(2)  # Wait for 1 second to load new content 
            
            # self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[3]')
            # time.sleep(2)  # Wait for 1 second to load new content 
            # self.LogScreenshot.fLogScreenshot(message=f"Results page - Part 2", pass_=True, log=True, screenshot=True)

            # Log mismatching columns and their values
            if matching_columns:
                for column, expected, actual in matching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Matching column '{column}': Expected({expected}), Actual({actual})",                                                
                                            pass_=True, log=True, screenshot=False)
            
            # Log mismatching columns and their values
            if mismatching_columns:
                for column, expected, actual in mismatching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                                pass_=False, log=True, screenshot=False)            

        except Exception as e:
            LogScreenshot.fLogScreenshot(
                message=f"Error in results validation: {e}",
                pass_=False, log=True, screenshot=True
            )
            tc_status.append("FAIL")
  
    def get_actual_results_from_page_DOM(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}       
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)
            # Assign specific key-value pairs based on column_to_key_mapping
            # actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['StatisticalDesign'] = Webpage_dict.get('StatisticalDesign', 'N/A')
            actual_results['Test'] = Webpage_dict.get('Test', 'N/A')
            actual_results['inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            actual_results['Hypothesis'] = Webpage_dict.get('Hypothesis', 'N/A')
            actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            actual_results['AllocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            actual_results['TestStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            actual_results['stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            actual_results['sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')            
            actual_results['power'] = Webpage_dict.get('Power', 'N/A')
            actual_results['probofSuccess'] = Webpage_dict.get('Probability of Success', 'N/A')        
            actual_results['variance'] = Webpage_dict.get('Variance', 'N/A')
            actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A') 
            actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')
            actual_results['priorDistributionFor'] = Webpage_dict.get('Prior Distribution for', 'N/A')
            actual_results['Assurance_distribution'] = Webpage_dict.get('Distribution Method', 'N/A')        
            actual_results['E(δ)'] = Webpage_dict.get('E(δ)', 'N/A')
            actual_results['SD(δ)'] = Webpage_dict.get('SD(δ)', 'N/A')
            actual_results['piParams_a'] = Webpage_dict.get('a', 'N/A')
            actual_results['piParams_b'] = Webpage_dict.get('b', 'N/A')
            actual_results['propCtrl'] = Webpage_dict.get('Proportion Under Control', 'N/A')
            actual_results['propTrmt'] = Webpage_dict.get('Proportion Under Treatment', 'N/A')
            actual_results['margin'] = Webpage_dict.get('Under H0', 'N/A')
            actual_results['diffInProp'] = Webpage_dict.get('Under H1', 'N/A') 
            actual_results['accrualRate'] = Webpage_dict.get('Avg. Subjects Enrolled (per Day)', 'N/A') 
            actual_results['UniformMin'] = Webpage_dict.get('Min', 'N/A') 
            actual_results['UniformMax'] = Webpage_dict.get('Max', 'N/A') 
     	
            
            actual_results['maxInfo'] = Webpage_dict.get('Information', 'N/A')
            actual_results['completers'] = Webpage_dict.get('Completers:', 'N/A')
            actual_results['accrualDuration'] = Webpage_dict.get('Accrual Duration', 'N/A')
            actual_results['studyDuration'] = Webpage_dict.get('Study Duration', 'N/A')
            actual_results['criticalPt'] = Webpage_dict.get('Critical Point', 'N/A')
            actual_results['diffInMeans'] = Webpage_dict.get('Under H1', 'N/A')   
            actual_results['ratioOfMeans'] = Webpage_dict.get('Under H1', 'N/A')  
            actual_results['meanRespNull'] = Webpage_dict.get('Mean Response under Null', 'N/A')
            actual_results['meanRespAlt'] = Webpage_dict.get('Mean Response under Alternative', 'N/A') 

            # actual_results['Assurance_inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            # actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A') for DOM this column repeates in result page, value going for droupctrl
            # actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')for DOM this column repeates, value going for drouptrtmnt
            # actual_results['dropoutsCtrl'] = Webpage_dict.get('Mean Control', 'N/A') Repeated column-DOM
            # actual_results['dropoutsTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')Repeated column-DOM
            # actual_results['sampleSizeTrmt'] = Webpage_dict.get('Treatment', 'N/A')
            # actual_results['sampleSizeCtrl'] = Webpage_dict.get('Control', 'N/A') 
            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results

    def get_actual_results_from_page_DOP(self):
        """
        Retrieve actual results from the results page and return as a dictionary.

        This method should be customized based on how actual results are extracted from your application's UI.

        Returns:
            dict: Dictionary containing actual results (column names mapped to their values).
        """
        actual_results = {}       
        try:
            # Assuming your provided code snippet correctly extracts key-value pairs from the webpage
            key_elements = self.base.findElements("Keyxpath")
            time.sleep(5)
            value_elements = self.base.findElements("Valuexpath")
            time.sleep(5)
            Webpage_dict = self.functionsforexcel.getalltheKeyValuepairofPage(Key_xpath=key_elements, Value_Xpath=value_elements)
            self.LogScreenshot.fLogScreenshot(message=f"Extracted key value pairs with Results page",
                                            pass_=True, log=True, screenshot=True)
            
            # Assign specific key-value pairs based on column_to_key_mapping
            actual_results['StudyObjective'] = Webpage_dict.get('Study Objective', 'N/A')
            actual_results['Phase'] = Webpage_dict.get('Phase', 'N/A')
            actual_results['TargetPopulation'] = Webpage_dict.get('Target Population', 'N/A')
            actual_results['ControlArm'] = Webpage_dict.get('Control Arm', 'N/A')
            actual_results['TreatmentArm'] = Webpage_dict.get('Treatment Arm', 'N/A')
            actual_results['Priority'] = Webpage_dict.get('Priority', 'N/A')
            actual_results['EndpointName'] = Webpage_dict.get('Endpoint Name', 'N/A')
            actual_results['EndpointType'] = Webpage_dict.get('Endpoint Type', 'N/A')
            actual_results['BetterResponse'] = Webpage_dict.get('Better Response', 'N/A')
            actual_results['FollowUpTime'] = Webpage_dict.get('Follow-up Time', 'N/A')
            actual_results['StatisticalDesign'] = Webpage_dict.get('StatisticalDesign', 'N/A')
            actual_results['Test'] = Webpage_dict.get('Test', 'N/A')
            actual_results['inputMethod'] = Webpage_dict.get('Input Method', 'N/A')
            actual_results['Hypothesis'] = Webpage_dict.get('Hypothesis', 'N/A')
            actual_results['TestType'] = Webpage_dict.get('Test Type', 'N/A')
            actual_results['AllocationRatio'] = Webpage_dict.get('Allocation Ratio', 'N/A')
            actual_results['TestStatistic'] = Webpage_dict.get('Test Statistic', 'N/A')
            actual_results['stdDeviation'] = Webpage_dict.get('Standard Deviation', 'N/A')
            actual_results['power'] = Webpage_dict.get('Power', 'N/A')
            actual_results['probofSuccess'] = Webpage_dict.get('Probability of Success', 'N/A')        
            actual_results['variance'] = Webpage_dict.get('Variance', 'N/A')
            actual_results['priorDistributionFor'] = Webpage_dict.get('Prior Distribution for', 'N/A')
            actual_results['Assurance_distribution'] = Webpage_dict.get('Distribution Method', 'N/A')        
            actual_results['E(δ)'] = Webpage_dict.get('E(δ)', 'N/A')
            actual_results['SD(δ)'] = Webpage_dict.get('SD(δ)', 'N/A')
            actual_results['piParams_a'] = Webpage_dict.get('a', 'N/A')
            actual_results['piParams_b'] = Webpage_dict.get('b', 'N/A')
            actual_results['propCtrl'] = Webpage_dict.get('Proportion Under Control', 'N/A')
            actual_results['propTrmt'] = Webpage_dict.get('Proportion Under Treatment', 'N/A')
            actual_results['margin'] = Webpage_dict.get('Under H0', 'N/A')
            actual_results['diffInProp'] = Webpage_dict.get('Under H1', 'N/A')   
            
            actual_results['sampleSize'] = Webpage_dict.get('Sample Size', 'N/A')  
            actual_results['maxInfo'] = Webpage_dict.get('Information', 'N/A')
            actual_results['completers'] = Webpage_dict.get('Completers:', 'N/A')
            actual_results['accrualDuration'] = Webpage_dict.get('Accrual Duration', 'N/A')
            actual_results['studyDuration'] = Webpage_dict.get('Study Duration', 'N/A')
            actual_results['criticalPt'] = Webpage_dict.get('Critical Point', 'N/A')
            actual_results['diffInMeans'] = Webpage_dict.get('Under H1', 'N/A')   
            actual_results['criticalPtLwr'] = Webpage_dict.get('Lower Critical Point', 'N/A')
            actual_results['criticalPtUpr'] = Webpage_dict.get('Upper Critical Point', 'N/A')   

            # actual_results['Assurance_inputMethod'] = Webpage_dict.get('Input Method', 'N/A') repeated column
            # actual_results['meanCtrl'] = Webpage_dict.get('Mean Control', 'N/A') for DOP this column value going for droupctrl
            # actual_results['meanTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')for DOP this column value going for drouptrtmnt
            # actual_results['dropoutsCtrl'] = Webpage_dict.get('Mean Control', 'N/A') Repeated column-DOP
            # actual_results['dropoutsTrmt'] = Webpage_dict.get('Mean Treatment', 'N/A')Repeated column-DOP
            # actual_results['sampleSizeTrmt'] = Webpage_dict.get('Treatment', 'N/A')taking data of completers
            # actual_results['sampleSizeCtrl'] = Webpage_dict.get('Control', 'N/A')taking data of completers instead of SS
            # actual_results['ratioOfMeans'] = Webpage_dict.get('Under H1', 'N/A')  
            # actual_results['meanRespNull'] = Webpage_dict.get('Mean Response under Null', 'N/A')
            # actual_results['meanRespAlt'] = Webpage_dict.get('Mean Response under Alternative', 'N/A') 
            
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error while extracting actual results: {e}",
                                            pass_=False, log=True, screenshot=True)
        return actual_results
    
    def validate_results_DOP(self, datafile, row_data, LogScreenshot, tc_status):
        """
        Validate the results page against the expected values from the datafile.

        Parameters:
            datafile (pd.DataFrame): DataFrame containing test data.
            row_data (pd.Series): Series containing row data from datafile DataFrame.
            LogScreenshot (cLogScreenshot): LogScreenshot instance for logging and capturing screenshots.
            tc_status (list): List to store test case status ('PASS' or 'FAIL').
        """
        try:
            
            # Retrieve actual results from the results page
            actual_results = self.get_actual_results_from_page_DOP()

            # Compare actual results with expected values (row_data)
            matching_columns = []
            mismatching_columns = []

            for column, expected_value in row_data.items():
                actual_value = actual_results.get(column, None)
                
                if actual_value is not None and actual_value != 'N/A' and expected_value != 'nan':
                    result = self.assert_passforSciChars(expected_value, actual_value)
                    print(result)
                    if self.check_if_is_number(actual_value) and self.check_if_is_number(expected_value):
                        actual_value = round(float(actual_value), 3)
                        expected_value = round(float(expected_value), 3)
                    else:
                        actual_value = str(actual_value)
                        expected_value = str(expected_value)

                    if str(actual_value) == str(expected_value) or result == "PASS":
                        matching_columns.append((column, expected_value, actual_value))
                        tc_status.append("PASS")
                    else:
                        mismatching_columns.append((column, expected_value, actual_value))
                        tc_status.append("FAIL")

            self.LogScreenshot.fLogScreenshot(message=f"Results page", pass_=True, log=True, screenshot=True)
            time.sleep(2)  # Wait for 1 second to load new content 
            
            # self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[3]')
            # time.sleep(2)  # Wait for 1 second to load new content 
            # self.LogScreenshot.fLogScreenshot(message=f"Results page - Part 2", pass_=True, log=True, screenshot=True)

            # Log mismatching columns and their values
            if matching_columns:
                for column, expected, actual in matching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Matching column '{column}': Expected({expected}), Actual({actual})",                                                
                                            pass_=True, log=True, screenshot=False)
            
            # Log mismatching columns and their values
            if mismatching_columns:
                for column, expected, actual in mismatching_columns:
                    LogScreenshot.fLogScreenshot(message=f"Mismatching column '{column}': Expected({expected}), Actual({actual})",
                                                pass_=False, log=True, screenshot=False)            

        except Exception as e:
            LogScreenshot.fLogScreenshot(
                message=f"Error in results validation: {e}",
                pass_=False, log=True, screenshot=True
            )
            tc_status.append("FAIL")

    def SelectAssurance_DistributionDropdown(self,DistributionMethod,UnivWaitFor=0):
        DistributionMethod=['Normal','Uniform','User Specified']
        if DistributionMethod=='Normal':
            self.base.selectByvisibleText('DistributionMethodDD','Normal')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Normal from Distribution Method option",
                    pass_ = True, log = True, screenshot = True)  
            self.base.verifyelement_displayed("Assur_InputmethodDD",UnivWaitFor=5)
            self.base.input_text_with_ctrlAltDel("eDeltaTB", 1,UnivWaitFor=4)
            self.base.input_text_with_ctrlAltDel("sDeltaTB", 1,UnivWaitFor=4)
            self.base.verifyelement_displayed("eDeltaTB",UnivWaitFor=5)
            self.base.verifyelement_displayed("sDeltaTB",UnivWaitFor=5)
            self.LogScreenshot.fLogScreenshot( message = f"Verified element display e&s Delta fields and feed data",
                    pass_ = True, log = True, screenshot = True)             
            
        elif DistributionMethod=='Uniform':
            self.base.selectByvisibleText('DistributionMethodDD','Uniform')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Uniform option from the DistributionMethod dropdown",
                    pass_ = True, log = True, screenshot = True)  
            
            self.base.input_text_with_ctrlAltDel("UniformMinTB", 1,UnivWaitFor=4)
            self.base.input_text_with_ctrlAltDel("UniformMaxTB", 1,UnivWaitFor=4)

        elif DistributionMethod=='User Specified':
                self.base.selectByvisibleText('DistributionMethodDD','User Specified')
                # Enable Assurance
                self.base.click("ChooseFileTB", UnivWaitFor=5)
                current_directory = os.getcwd()
                print("Current working directory:", current_directory)
                file_name = "Samplecsv.csv"
                file_path = os.path.join(current_directory, file_name)

                print("File path:", file_path)
                self.LogScreenshot.fLogScreenshot( message = f"Selected User Specified option from the DistributionMethod dropdown",
                        pass_ = True, log = True, screenshot = True) 

                self.base.click("ChooseFileTB")
                time.sleep(2)
                # pyautogui.write(file_path)
                # time.sleep(2)
                # pyautogui.press('enter')

    def process_input_row_MOPR(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            InputMethod = row_data['InputMethod']
            self.process_input_row_generic_MOPR_MOPD(row_data,WhatToCompute) 
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'])
            self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')           
            self.base.selectByvisibleText("InputMethod", row_data['InputMethod'])
            time.sleep(2)     
            if row_data['Hypothesis'] == 'Superiority' and InputMethod == "Ratio of Means" and WhatToCompute != "Ratio of Means":
                self.fill_input_field('RatioofMeansTB', row_data, 'input_ratioOfMeans', 'Enter The value in Ratio of Means Field ')
            elif InputMethod == "Individual Means":
                self.fill_input_field('MeanControlTB', row_data, 'meanCtrl', 'Enter The value in Mean Control Field ')
                self.fill_input_field('MeanTreatmentTB', row_data, 'meanTrmt', 'Enter The value in Mean Treatment Field ')                
            if (row_data['Hypothesis'] == 'Noninferiority'):
                self.fill_input_field('Noninferiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
                if InputMethod == "Ratio of Means" and WhatToCompute != "Ratio of Means":
                    self.fill_input_field('RatioofMeansNITB', row_data, 'input_ratioOfMeans', 'Enter The value in Ratio of Means Field ')
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided",
                                        pass_=True, log=True, screenshot=True)
            self.base.selectByvisibleText("TestStatisticDD", row_data['TestStatistic']) 
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided'", pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for MOPR {e}", pass_=False, log=True, screenshot=True)
    
    def process_input_row_MOPD(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            WhatToCompute = row_data['WhatToCompute']
            InputMethod = row_data['InputMethod']
            TestType = row_data['TestType']
            self.process_input_row_generic_MOPR_MOPD(row_data,WhatToCompute) 
            self.base.selectByvisibleText("TestTypeDD", row_data['TestType'],UnivWaitFor=5)
            
            self.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')           
            if (TestType == '2-Sided (Asymmetric)'):
                    self.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
                    self.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field')
            self.base.selectByvisibleText("InputMethod", row_data['InputMethod'],UnivWaitFor=4)
            time.sleep(2)     
            if InputMethod == "Difference of Means" and WhatToCompute != "Diff. in Means":
                self.fill_input_field('DifferenceofMeansPairedDataTB', row_data, 'input_diffInMeans', 'Enter The value in Difference of Means Field ')
            elif InputMethod == "Individual Means":
                self.fill_input_field('MeanControlTB', row_data, 'meanCtrl', 'Enter The value in Mean Control Field ')
                self.fill_input_field('MeanTreatmentTB', row_data, 'meanTrmt', 'Enter The value in Mean Treatment Field ')                
            if (row_data['Hypothesis'] == 'Noninferiority'):
                self.fill_input_field('Noninferiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided",
                                        pass_=True, log=True, screenshot=True)
            self.base.selectByvisibleText("TestStatisticDD", row_data['TestStatistic'],UnivWaitFor=4) 
            if (str(int(row_data['compAssurance'])) == '1'):
                # Calling the common assurance input method for DOM & MOPD
                time.sleep(5)
                self.process_DOM_MOPD_Assurance(row_data)
            self.LogScreenshot.fLogScreenshot(message=f"All Design Inputs provided'", pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering inputs for MOPD {e}", pass_=False, log=True, screenshot=True)
    
    def process_DOM_MOPD_Assurance(self, row_data):
        self.base.click("IncludeAssurance",UnivWaitFor=4)
        self.LogScreenshot.fLogScreenshot(message=f"Clicked on Assurance toggle", pass_=True, log=True, screenshot=True)
        self.base.selectByvisibleText("DistributionMethodDD", row_data['Assurance_distribution'])   
        if ((row_data['Assurance_distribution'] == 'Normal')):
            self.base.selectByvisibleText("Assur_InputmethodDD", row_data['Assurance_inputMethod'],UnivWaitFor=5)
            if (row_data['Assurance_inputMethod'] == 'E(δ) and SD(δ)'):
                self.fill_input_field('eDeltaTB', row_data, 'eDelta', 'Enter The value in eDelta Field :')
                self.fill_input_field('sdDeltaTB', row_data, 'sdDelta', 'Enter The value in sdDelta Field :')
                time.sleep(5)   
            if (row_data['Assurance_inputMethod'] == 'Percentiles of δ'):                
                self.base.selectByvisibleText("percDelta1stOperator", row_data['sign1'])
                self.base.selectByvisibleText("percDelta2ndOperator", row_data['sign2'])                    
                self.fill_input_field('percDelta1stPercentileVal', row_data, 'PercentileVal1', 'Enter The value in percDelta1stPercentileVal Field :')
                self.fill_input_field('percDelta1stPercentileProb', row_data, 'PercentileProb1', 'Enter The value in percDelta1stPercentileProb Field :')
                self.fill_input_field('percDelta2ndPercentileVal', row_data, 'PercentileVal2', 'Enter The value in percDelta2stPercentileVal Field :')
                self.fill_input_field('percDelta2ndPercentileProb', row_data, 'PercentileProb2', 'Enter The value in percDelta2stPercentileProb Field :')
            if (row_data['Assurance_inputMethod'] == 'Percentiles of δ/σ'):
                self.base.selectByvisibleText("percDeltaBySigma1stOperator", row_data['sign1'])
                self.base.selectByvisibleText("percDeltaBySigma2ndOperator", row_data['sign2'])
                self.fill_input_field('percDeltaBySigma1stPercentileVal', row_data, 'PercentileVal1', 'Enter The value in percDeltaBySigma1stPercentileVal Field :')
                self.fill_input_field('percDeltaBySigma1stPercentileProb', row_data, 'PercentileProb1', 'Enter The value in percDeltaBySigma1stPercentileProb Field :')
                self.fill_input_field('percDeltaBySigma2ndPercentileVal', row_data, 'PercentileVal2', 'Enter The value in percDeltaBySigma2stPercentileVal Field :')
                self.fill_input_field('percDeltaBySigma2ndPercentileProb', row_data, 'PercentileProb2', 'Enter The value in percDeltaBySigma2stPercentileProb Field :')
        if (row_data['Assurance_distribution'] == 'Uniform'):
            self.fill_input_field('UniformMinTB', row_data, 'UniformMin', 'Enter The value in UniformMin Field :')
            self.fill_input_field('UniformMaxTB', row_data, 'UniformMax', 'Enter The value in UniformMax Field :')  
            time.sleep(5)          
            self.LogScreenshot.fLogScreenshot(message=f"All Assurance Inputs provided'", pass_=True, log=True, screenshot=True)
    