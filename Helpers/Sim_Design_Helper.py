import time
import pandas as pd
from Helpers import ExcelHelper
from Helpers.Base import Base 
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions
from Helpers.ExcelHelper import Excel_HelperFunctions
from Helpers.PlanCreationHelper import PlanCreationHelper
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Sim_DesignPageHelperfunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.input_field= AD_DesignPageHelperfunctions(self.driver,self.extra)       
    
    def verify_elements_AnalyticalDesign(self,row_index):            
            """
                Helper function to verify the presence, visibility, disabled state, and text content of a web element.
            Returns:
                bool: True if the element is present, visible, disabled, and contains the expected text; False otherwise.
            """
            elements= ['HypothesisDD',
                        'SampleSizeTB',
                        'AllocationRatioTB',
                        'TestStatisticDD',
                        'RandomizedDD',
                        'VarianceDD',
                        'TestTypeDD',
                        'CriticalPointTB'
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
            Disabledelements= ['HypothesisDD',
                        'TestTypeDD']
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

    def Select_RandomizedMethod(self,Inputmethod,UnivWaitFor=0):
        Inputmethod=['Fixed Allocation','Complete Randomized Design']
        if Inputmethod=='Fixed Allocation':
            self.base.selectByvisibleText('RandomizedDD','Fixed Allocation')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Fixed Allocation from the RandomizedMethod dropdown",
                    pass_ = True, log = True, screenshot = True)  
        elif Inputmethod=='Complete Randomized Design':
            self.base.selectByvisibleText('RandomizedDD','Complete Randomized Design')
            # Enable Assurance
            self.LogScreenshot.fLogScreenshot( message = f"Selected Complete Randomized Design option from the RandomizedMethod dropdown",
                    pass_ = True, log = True, screenshot = True)
        
    def Select_teststatistic(self,teststatistic,variance,UnivWaitFor=0):
        if teststatistic=='Z':
            self.base.selectByvisibleText('TestStatisticDD','Z')
            self.base.input_text_with_ctrlAltDel('StandardDeviationTB','1')
            self.LogScreenshot.fLogScreenshot( message = f"Selected Z option from teststatistic dropdown",
                    pass_ = True, log = True, screenshot = True)  
        elif teststatistic=='t':
            self.base.selectByvisibleText('RandomizedDD','Complete Randomized Design')
            self.LogScreenshot.fLogScreenshot( message = f"Selected Complete Randomized Design option from the RandomizedMethod dropdown",
                    pass_ = True, log = True, screenshot = True)
            self.base.selectByvisibleText("VarianceDD", variance, UnivWaitFor=3)

    def perform_input_actionsAnalyticalDesign(self, option, LogScreenshot):
        # Example: Implement actions to interact with the input page using row_data
        self.base.click("designs_link",UnivWaitFor=5)
        self.Select_RandomizedMethod("Individual", UnivWaitFor=5)
        self.base.selectByvisibleText("VarianceDD",option,UnivWaitFor=4)

    def process_Sim_input_row_DOM_Design(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:         
            self.input_field.fill_input_field_nonfloat('SampleSizeTB', row_data, 'simInput_sampleSize', 'Enter The value in simInput_sampleSize Field :')
            self.input_field.fill_input_field('AllocationRatioTB', row_data, 'simInput_allocationRatio', 'Enter The value in simInput_allocationRatio Field :')
            self.input_field.fill_input_field('CriticalPointTB', row_data, 'simInput_criticalPt', 'Enter The value on critical point Field ')
            self.base.selectByvisibleText("TestStatisticDD", row_data['simInput_testStatistic'])
            time.sleep(3)
            if row_data['simInput_testStatistic'] == 'Z':
                self.input_field.fill_input_field('StandardDeviationTB', row_data, 'simInput_stdDeviation', 'Enter The value on standardDeviation Field ')
            if (row_data['Hypothesis'] == 'Noninferiority'):
                self.input_field.fill_input_field('Noninferiority_Margin', row_data, 'simInput_margin', 'Enter The value in simInput_margin Field :')           
            if (row_data['Hypothesis'] == 'Super Superiority'):
                self.input_field.fill_input_field('SuperSuperiority_Margin', row_data, 'margin', 'Enter The value in margin Field ')            

            self.LogScreenshot.fLogScreenshot( message = f"input to design page is Complete",
                    pass_ = True, log = True, screenshot = True)
        except Exception as e:
              self.LogScreenshot.fLogScreenshot(message=f"Error while feeding inputs: {e}",
                                            pass_=False, log=True, screenshot=True)
      
    def process_Sim_input_row_SingleProportion_Design(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """       
        TestType = row_data['TestType']                       
        self.input_field.fill_input_field('propResponseUnderNull', row_data, 'siminput_propResponseUnderNull', 'Enter The value in propResponseUnderNull Under Null Field ')
        self.input_field.fill_input_field('StandardDeviationTB', row_data, 'stdDeviation', 'Enter The value in Standard Deviation Field ')
        if (TestType == '2-Sided (Asymmetric)'):
            self.input_field.fill_input_field('upperType1Error', row_data, 'typeIErrorUpr', 'Enter The value in upperType1Error Field')
            self.input_field.fill_input_field('lowerType1Error', row_data, 'typeIErrorLwr', 'Enter The value in lowerType1Error Field')
        time.sleep(2)                



      