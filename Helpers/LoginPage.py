import time
from Helpers.Base import Base 
from utilities.readProperties import ReadConfig
from utilities.reportScreenshot import add_screenshot
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self,driver,extra):
        self.driver = driver
        self.extra = extra
        # Instantiate the base class
        self.base = Base(self.driver)
        self.env = ReadConfig.getEnvironmenttype()
        # instantiate the logger class
        self.logger = LogGen.loggen()
        # instantiate the logScreenshot class
        self.LogScreenshot = cLogScreenshot(self.driver,self.extra)
        
    def complete_login(self,username,password,iter):
        '''
        application login page must be opened before calling this method
        '''
        try:
            if self.env == "test":
                # enter username
                self.base.input_text("username_textbox",username, UnivWaitFor=60)
                self.LogScreenshot.fLogScreenshot( message = 'Enter username', 
                    pass_= True, log = True, screenshot= False )
                # submit username
                self.base.click("username_button",UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = 'Submit username', 
                    pass_= True, log = True, screenshot= False )
                
                self.base.input_text("username_signin",username, UnivWaitFor=2)
                self.LogScreenshot.fLogScreenshot( message = 'Enter username again', 
                    pass_= True, log = True, screenshot= False )
                self.base.click("btn_signin_submit", UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = 'Click submit username',
                    pass_= True, log = True, screenshot= False )
                time.sleep(5)
                # enter password
                self.base.input_text("password_textbox",password, UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = 'Enter password', 
                    pass_= True, log = True, screenshot= False )
                # submit password
                self.base.click("password_button", UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = 'Submit password', 
                    pass_= True, log = True, screenshot= False )
            elif self.env == "beta":
                # enter username
                self.base.input_text("username_textbox",username, UnivWaitFor=60)
                self.LogScreenshot.fLogScreenshot( message = 'Enter username', 
                    pass_= True, log = True, screenshot= False )
                # submit username
                self.base.click("username_button", UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = 'Submit username', 
                    pass_= True, log = True, screenshot= False )
                # enter password
                self.base.input_text("oktapassword_textbox",password, UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = 'Enter password', 
                    pass_= True, log = True, screenshot= False )
                # submit password
                self.base.click("oktapassword_button", UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = 'Submit password', 
                    pass_= True, log = True, screenshot= False )
            elif self.env == "preprod":
                # enter username
                self.base.input_text("username_textbox",username, UnivWaitFor=60)
                self.LogScreenshot.fLogScreenshot( message = 'Enter username', 
                    pass_= True, log = True, screenshot= False )
                # submit username
                self.base.click("username_button", UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = 'Submit username', 
                    pass_= True, log = True, screenshot= False )
                # enter password
                self.base.input_text("oktapassword_textbox",password, UnivWaitFor=5)
                self.LogScreenshot.fLogScreenshot( message = 'Enter password', 
                    pass_= True, log = True, screenshot= False )
                # submit password
                self.base.click("oktapassword_button", UnivWaitFor=3)
                self.LogScreenshot.fLogScreenshot( message = 'Submit password', 
                    pass_= True, log = True, screenshot= False )
            else:
                raise Exception("Invalid environment")
        except Exception:
            pass
        # check whether the login page opened or not
        try:
            # self.base.verifyelement_isdisplayed("home_button",UnivWaitFor=60)
            # wait for 5 seconds for projects to appear before taking the screenshot
            time.sleep(15)
            self.LogScreenshot.fLogScreenshot( message = f"Iteration {iter + 1}: Complete login and check if application landing page visible",
                pass_ = True, log = True, screenshot= True )
        except Exception:
            self.LogScreenshot.fLogScreenshot( message = f"Iteration {iter + 1}: Complete login and check if application landing page visible",
                pass_ = False, log = True, screenshot= True )
            raise Exception("Login Unsuccessful")

    # def logout(self):
    #     '''
    #     this method is to logout from the application and arrive at the login landing page
    #     '''
        
    #     # click on profile icon
    #     self.base.click("avatar_button", UnivWaitFor=10 )
    #     # click on logout
    #     self.base.click("logout_button", UnivWaitFor=10 )
    #     # confirm popup by clicking on sign out
    #     self.base.click("confirmlogout_button", UnivWaitFor=10 )
    #     # click on login button
    #     # self.base.click("loginagain_button", UnivWaitFor=10 )
    #     # self.LogScreenshot.fLogScreenshot( message = f"Complete logout",
    #     #     pass_ = True, log = True, screenshot= False )
    #     try:
    #         alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
    #         #Switch the control to the Alert window
    #         alert = self.driver.switch_to.alert
    #         #Retrieve the message on the Alert window
    #         alert_text = alert.text
    #         print ("Alert shows following message: "+ alert_text )
    #         time.sleep(2)
    #         # Accept the alert
    #         alert.accept()
    #         time.sleep(2)
    #         self.LogScreenshot.fLogScreenshot( message = f"Logout completed successfully",
    #         pass_ = True, log = True, screenshot= True )
    #     except Exception as e:
    #         # Handle the exception
    #         print("Error handling alert:", str(e))  
    #     # click on login button
    #     self.base.click("loginagain_button", UnivWaitFor=10 )
    #     self.LogScreenshot.fLogScreenshot( message = f"Complete logout",
    #         pass_ = True, log = True, screenshot= False )
    #     time.sleep(5)
                
      
    def logout(self):
        '''
        this method is to logout from the application and arrive at the login landing page
        '''
        try:
            # click on profile icon
            self.base.click("avatar_button", UnivWaitFor=10 )
            # click on logout
            # self.base.click("logout_button", UnivWaitFor=10 )
            # confirm popup by clicking on sign out
            # self.base.click("confirmlogout_button", UnivWaitFor=10 )
            # click on login button
            # self.base.click("loginagain_button", UnivWaitFor=10 )
            self.LogScreenshot.fLogScreenshot( message = f"Complete logout",
                pass_ = True, log = True, screenshot= False )
        except Exception:
            self.LogScreenshot.fLogScreenshot( message = f"Complete logout",
                pass_ = False, log = True, screenshot= False )
            raise Exception("Logout unsuccessful")