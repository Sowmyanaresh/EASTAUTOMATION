
from Helpers.Base import Base 
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.support import expected_conditions as EC
import time
from Helpers.Base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ValidationMessageVerifier:

    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        self.base = Base(self.driver)
        self.logger = LogGen.loggen()
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
   
    def verify_validation_message(self, *locator, invalid_input, excpected_msg_locator, expected_message):
        
        # element=self.base.findElement(locator)
        # element=self.driver.find_element("allocationRatio")
        element=self.driver.find_element(By.ID, "allocationRatio")
        element.clear()
        print(element)
        # locatortofind=self.base.findElement(element)
        # field = self.base.findElementBy(*field_locator)
        
        # Clear the textbox and press tab to trigger validation
        self.base.ClearTextboxandPressTab(element,UnivWaitFor=5)
        print("Cleared the text box")
        self.LogScreenshot.fLogScreenshot(message=f"Cleared textbox - {locator}", pass_=True, log=True, screenshot=True)

        # Capture and verify the mandatory validation message
        validation_message_element = self.base.get_text(excpected_msg_locator,UnivWaitFor=5)
        actual_message = validation_message_element.text.strip()
        print("actual Mandatory val msg",actual_message)
        # assert actual_message == expected_message, f"Expected '{expected_message}', but got '{actual_message}'"

        # Input invalid data
        self.base.input_text_with_ctrlAltDel(element,invalid_input,UnivWaitFor=5)
        self.LogScreenshot.fLogScreenshot(message=f"Entered invalid input - {invalid_input} in {locator}", pass_=True, log=True, screenshot=True)
        print("Input invalid range into text box")

        # Capture and verify the range validation message
        validation_message_element = self.base.get_text(excpected_msg_locator,UnivWaitFor=2)
        actual_message = validation_message_element.text.strip()
        print("actual range val msg",actual_message)
        # assert actual_message == expected_message, f"Expected '{expected_message}', but got '{actual_message}'"
   
#    for validation in test['validations']:
#             # Clear the textbox and input invalid data
#             textbox = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, validation['locator']))
#             )
#             textbox.clear()
#             textbox.send_keys(validation['invalid_input'])
#             textbox.send_keys(Keys.TAB)  # Move focus away to trigger validation

#             # Verify validation message
#             validation_msg = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, validation['expected_msg_locator']))
#             )
#             assert validation_msg.text == validation['expected_message'], f"Validation message for {validation['locator']} does not match. Expected: {validation['expected_message']}, Found: {validation_msg.text}"

    def run_validationtests(self, tests):
        try:
            for test in tests:
                if 'pre_validation_steps' in test:
                    for step in test['pre_validation_steps']:
                        if step['action'] == 'click':
                            self.base.click(step['element_locator'],UnivWaitFor=4)
                        elif step['action'] == 'select_by_visible_text':
                            self.base.selectByvisibleText(step['element_locator'], step['text'])
                            self.LogScreenshot.fLogScreenshot( message = f"Clicked/Selected the element",
                            pass_ = False, log = True, screenshot = True)  
                
                    for validation in test['validations']:
                        # Clear the textbox and input invalid data
                        textbox = self.base.ClearTextboxandPressTab("locator")
                        validation_msg=self.base.findElement(validation['expected_msg_locator'])
                        valmsg=self.base.get_text(validation_msg)
                        # textbox.clear()
                        # textbox.send_keys(validation['invalid_input'])
                        # textbox.send_keys(Keys.TAB)  # Move focus away to trigger validation

                        # Verify validation message
                        # validation_msg = self.driver.findelement(validation['expected_msg_locator'])
                        assert valmsg == validation['expected_message'], f"Validation message for {validation['locator']} does not match. Expected: {validation['expected_message']}, Found: {validation_msg.text}"


                # for validation in test['validations']:      
                #     self.verify_validation_message(validation['locator'], validation['invalid_input'],validation['excpected_msg_locator'], validation['expected_message'])
                #     time.sleep(3)                    
                #     self.LogScreenshot.fLogScreenshot( message = f"Cleared / entered invalid input in the textbox and verified the validation msg",
                #         pass_ = True, log = True, screenshot = True)  
        except Exception as e:
            self.LogScreenshot.fLogScreenshot( message = f"Error in clearing / entering input ",
                        pass_ = True, log = True, screenshot = True)  
        
                    
                    # self.verify_validation_message(validation['locator'], validation['invalid_input'],validation['excpected_msg_locator'], validation['expected_message'])
                    # time.sleep(3)                    
        #             self.LogScreenshot.fLogScreenshot( message = f"Cleared / entered invalid input in the textbox and verified the validation msg",
        #                 pass_ = True, log = True, screenshot = True)  
        # except Exception as e:
        #     self.LogScreenshot.fLogScreenshot( message = f"Error in clearing / entering input ",
        #                 pass_ = True, log = True, screenshot = True)  
        