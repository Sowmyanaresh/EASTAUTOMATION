import time
import pandas as pd
from Helpers.Base import Base 
from Helpers.Ad_Design_Helper import AD_DesignPageHelperfunctions
from Helpers.ExcelHelper import Excel_HelperFunctions
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.common.exceptions import NoSuchElementException

class Sim_SimulationSetupPageHelperFunctions:
    
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        self.functionsforexcel = Excel_HelperFunctions(self.driver, extra)
        self.input_field= AD_DesignPageHelperfunctions(self.driver,self.extra)
    
    def process_Sim_input_row_SimulationSetup(self, row_data):
        """
        Process input data from a row of the datafile DataFrame.

        Parameters:
            row_data (pd.Series): Series containing row data from datafile DataFrame.
        """
        try:
          
            self.input_field.fill_input_field_nonfloat('NumofSimRunTB', row_data, 'simInput_numOfSims', 'Enter The value in simInput_numOfSims Field ')
            self.base.selectByvisibleText("RandomSeedDD",'Fixed',UnivWaitFor=8)
            self.input_field.fill_input_field_nonfloat('fixedSeed', row_data, 'simInput_seedVal', 'Enter The value on simInput_seedVal Field ')
            self.LogScreenshot.fLogScreenshot(message="Entered Num of sim and fixed seed value", pass_=True, log=True, screenshot=True)        

            self.base.click("Savebutton", UnivWaitFor=5)
            self.LogScreenshot.fLogScreenshot(message="Clicked on Save button", pass_=True, log=True, screenshot=True)
            self.base.click("SaveSimulate", UnivWaitFor=5)
            self.LogScreenshot.fLogScreenshot(message="Clicked on Save&Simulate button", pass_=True, log=True, screenshot=True)
            self.base.click("Simulatebutton", UnivWaitFor=10)
            self.LogScreenshot.fLogScreenshot(message="Clicked on Simulatebutton button", pass_=True, log=True, screenshot=True)        
            # self.base.click("ResultSet1", UnivWaitFor=5)     
            print("********************* Simulation is completed***************")

        except Exception as e:
            raise Exception(f"Error processing input row: {e}")