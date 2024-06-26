import time
from Helpers.Base import Base 
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
import pandas as pd
# import cv2
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class NewInputHelper:

    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()

        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)

    def create_new_inputSet(self,iter,rowdata):
        '''
        This method creates the collection with rule type
        '''
        try:
            
            self.base.click("Project_InputsLink")
            time.sleep(3)
            self.base.click("NewInputSetButton")
            time.sleep(5)
            # self.base.selectByvisibleText("Explore Designs") write a code to select inputset based on need,
            # store them in list and pick based on need 
            self.base.click("DesignButton",UnivWaitFor=5)       
            self.base.selectByvisibleText("SelectTest", rowdata['Test'])
            self.base.click("ContinueButton",UnivWaitFor=5)
            self.LogScreenshot.fLogScreenshot( message = f"Created New Input Set for Generate Design succesfully",
                pass_ = True, log = True, screenshot= True )
            # self.base.assertPageTitle("Solara",UnivWaitFor=60)
            # wait for 5 seconds for projects to appear before taking the screenshot
            time.sleep(5)
            self.LogScreenshot.fLogScreenshot( message = f"Iteration {iter}: New Input creation is succesfull",
                pass_ = True, log = True, screenshot= True )
            print("Input creation successful", iter)
        except Exception:
            self.LogScreenshot.fLogScreenshot( message = f"Iteration {iter}: New input is not created",
                pass_ = False, log = True, screenshot= True )
            raise Exception("Input creation Unsuccessful")
                
    def platformPageNavigations( self, locator,platformPageName):
        try:
        #    ther than mappingfile may be breaking in this try block
            if section == 'overview':
                section = "O"
            elif section == 'Results':
                section = "R"
            elif section == 'Compare':
                section = "C"
            else: 
                self.LogScreenshot.fLogScreenshot( message = f'Section not found in UI ',
                    pass_= False, log = True, screenshot= False )
                raise Exception( f'Section not found in mapping file - {section}' )

            platformPageName = str( '{"index":"' + locator + '::dropdown::' + section + '","type"}')
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f' for the parameter  - {e}',
                pass_= False, log = True, screenshot= False )
           
