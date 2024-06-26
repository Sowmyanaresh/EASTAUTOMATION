import time
import pandas as pd
from Helpers.Base import Base 
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions
from Helpers.ExcelHelper import Excel_HelperFunctions
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Sim_ResponsePageHelperFunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.input_field= AD_DesignPageHelperfunctions(self.driver,self.extra)  

    def verify_elements_AnalyticalResponse(self,row_index):
            
            """
                Helper function to verify the presence, visibility, disabled state, and text content of a web element.
            Returns:
                bool: True if the element is present, visible, disabled, and contains the expected text; False otherwise.
            """
            self.base.click("CommonStdCB",UnivWaitFor=3)
            elements= ['MeanControl_TB',
                       'Meantreatment_TB',
                       'SdcontrolTB',
                       'ProbabilityofdropoutTB',
                       'SDTreatmentTB'
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
            Disabledelements= ['DistributionDD',
                        'InputMethod']
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

    def process_Sim_input_row_Response(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.

        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
            self.input_field.fill_input_field('MeanTreatmentTB', row_data, 'simInput_meanTrmt', 'Enter The value in Mean Treatment Field ')
            self.input_field.fill_input_field('MeanControlTB', row_data, 'simInput_meanCtrl', 'Enter The value in Mean control Field ')
            self.input_field.fill_input_field('SdcontrolTB', row_data, 'simInput_stdDeviationCtrl', 'Enter The value in SD control Field ')
            
            if (row_data['Hypothesis'] == 'Noninferiority'):
                self.input_field.fill_input_field('ProbabilityDropoutTB', row_data, 'simInput_probOfDropout', 'Enter The value on Probability dropout Field ')

            # if self.base.CommonStdCB -yet to code this part( if the checkbox unchecked then need to enter below textbox)
            # self.input_field.fill_input_field('SDTreatmentTB', row_data, 'simInput_stdDeviationTrmt', 'Enter The value in sDelta Field ')
            self.LogScreenshot.fLogScreenshot( message = f"Input to Response page is Complete",
                    pass_ = True, log = True, screenshot = True)

        except Exception as e:
            raise Exception(f"Error processing input row: {e}")

    def process_Sim_input_row_Response_SingleProportion(self, row_data):
        
        self.input_field.fill_input_field('propResponseUnderAlt', row_data, 'simInput_propResponseUnderAlt', 'Enter The value in propResponseUnderAlt under Alternative Field ')                
        self.LogScreenshot.fLogScreenshot( message = f"Input to Response page is Complete",
                    pass_ = True, log = True, screenshot = True)   