import time
import pandas as pd
from Helpers.Base import Base 
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Sim_EnrollmentPageHelperFunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.input_field= AD_DesignPageHelperfunctions(self.driver,self.extra)
    
    def verify_elements_AnalyticalEnrollment(self,tc_index):
            
            """
                Helper function to verify the presence, visibility, disabled state, and text content of a web element.
            Returns:
                bool: True if the element is present, visible, disabled, and contains the expected text; False otherwise.
            """
            elements= ['EnrollmentType',
                        'AccrualModelDD',
                        'EnrollinputmethodDD',
                        'StartAtTimeTB',
                        'AvgSubTB',
                        'StartAtTimeTB2',
                        'AvgSubTB2'
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

            Disabledelements= ['EnrollmentType',
                        'AccrualModelDD',
                        'EnrollinputmethodDD',
                        'StartAtTimeTB']
            try:
                for elementid in Disabledelements:
                    if self.base.isdisabled(elementid):
                        print(elementid, ": is disabled")
                        self.LogScreenshot.fLogScreenshot( message = f"{elementid} is disabled as expected",
                        pass_ = True, log = True, screenshot = True)
                        return True
            except Exception as e:
                    print(f"Element '{elementid}' is not disabled on the webpage.")
           
            try:
                elementtext=self.base.get_text(elementid)
                if elementtext=="Global":
                        print(elementtext)
                        return True
            except Exception as e:
                    print(f"Element '{element_id}' text is not as expected on the webpage.")    

    def process_input_rowAnalyticalEnrollment(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.
        """
        try:
            
            # self.fill_input_field('SampleSizeTB', row_data, 'input_sampleSize', 'Enter The value in sampleSize Field :')
            self.input_field.fill_input_field('AvgSubTB', row_data, 'AllocationRatio', 'Enter The value in Allocation Ratio Field :')
            self.input_field.fill_input_field('StartAtTimeTB2', row_data, 'input_typeIError', 'Enter The value in type1error Field')
            self.input_field.fill_input_field('AvgSubTB2', row_data, 'input_power', 'Enter The value in Power Field :')    
        except Exception as e:
            raise Exception(f"Error processing input row: {e}")

    def process_input_row_Sim_enrollement(self, row_data):
        try:
            self.base.click("Enrollment_leftpanellink",UnivWaitFor = 10)
            if (str(int(row_data['simInput_includeAccrualDropout']))== '1'):
                    # if self.base.check_elementnotexists_by_xpath('EnrollmentAvgSubTB'):
                        self.base.click("EnrollmentToggle", UnivWaitFor=5)
                        self.LogScreenshot.fLogScreenshot(message=f"Toggled Enrollment",
                                        pass_=True, log=True, screenshot=True)
                    # else:
                        self.input_field.fill_input_field('EnrollmentAvgSubTB', row_data, 'simInput_accrualRate', 'Enter The value in accrualRate Field ')
                        self.LogScreenshot.fLogScreenshot(message=f"All Enrollment Inputs provided",
                                        pass_=True, log=True, screenshot=True)
        except Exception as e:
            self.LogScreenshot.fLogScreenshot(message=f"Error in entering Sim enrollment inputs{e}", pass_=False, log=True, screenshot=True)
    
    