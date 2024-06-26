from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Helpers.Base import Base 
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot

class RadioButtonHelper:
    
    def __init__( self, driver, extra):
        self.driver = driver
        self.base = Base( self.driver )
        self.extra = extra
        self.LogScreenshot = cLogScreenshot( self.driver,self.extra )

    def find_elements(self):
        locator="//label[contains(@for,'inline-')]"
        self.radio_buttons = self.base.findElements(locator)     
        
    def verify_text_box_display(self, textboxes):
        # Iterate through each radio button
        self.text_boxes= textboxes
        for i, radio_button in enumerate(self.radio_buttons):
            # Click on the radio button
            radio_button.click()

            # Wait for the corresponding text box to be visible
            WebDriverWait(self.driver, 10).until(EC.visibility_of(self.text_boxes[i]))

            # Verify if the text box is displayed
            if self.text_boxes[i].is_displayed():
                print(f"Text box {i+1} is displayed after clicking radio button {i+1}")
                # Check if the text box is disabled with the text 'Computed'
                if self.text_boxes[i].get_attribute('value') == 'Computed':
                    print(f"Text box {i+1} is disabled with the text 'Computed'")
            else:
                print(f"Text box {i+1} is not displayed after clicking radio button {i+1}")
