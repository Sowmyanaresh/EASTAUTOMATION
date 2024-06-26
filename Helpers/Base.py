from multiprocessing.connection import wait
from tkinter import Y
from selenium import webdriver
import time,os
import datetime
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


# decorator to wait for action to be executed
def fWaitFor(input_func):
    @functools.wraps(input_func)
    def wrapper(*args, **kwargs):
        try:
            UnivWaitFor = kwargs['UnivWaitFor']
        except KeyError:
            UnivWaitFor = 0
        # simply return the decorated function if waitFor argument isn't explicitly provided
        if UnivWaitFor == 0:
            return input_func(*args, **kwargs)
        # else ignore any error till {UnivWaitFor} seconds. If the functions executes, return the function's output
        else:  
            errorPresent = True
            timePassed = 0
            while errorPresent == True and timePassed < UnivWaitFor:
                try:
                    result = input_func(*args, **kwargs)
                    errorPresent = False
                    return result 
                except Exception:
                    timePassed += 1
                    time.sleep(1)
            # if function fails even after {UnivWaitFor} seconds, return the error as is 
            if errorPresent == True:
                return input_func(*args, **kwargs)

    return wrapper


class Base:
    '''
    IMPORTANT: The OR file should contain valid locator types. Eg: ID, XPATH, NAME, etc.
    Refer https://selenium-python.readthedocs.io/locating-elements.html for more information on valid locator types
    '''
    

    def __init__(self, driver):
        self.driver = driver

    # read object repository csv to get a list of lists
    @fWaitFor
    def read_data_from_csv(self,filename,UnivWaitFor = 0):
        df = pd.read_csv(filename)
        return df
    @fWaitFor
    def read_data_from_excel(self,filename,UnivWaitFor = 0):
        df = pd.read_excel(filename)
        return df

    # identify locatorpath from locationname-object in csv
    @fWaitFor
    def locatorpath(self,locatorname,UnivWaitFor = 0):
        df = self.read_data_from_csv(ReadConfig.getORFilePath())
        return df.loc[df['Object']==locatorname]['Path'].to_list()[0]

    # identify locatortype from locationname-object in csv
    @fWaitFor
    def locatortype(self,locatorname,UnivWaitFor = 0):
        df = self.read_data_from_csv(ReadConfig.getORFilePath())
        return df.loc[df['Object']==locatorname]['Type'].to_list()[0]

    # click a web element using locatorname
    @fWaitFor
    def click(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and click on the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()

    # click an element inside a container using locatornames 
    @fWaitFor
    def clickInside(self,container,locator,UnivWaitFor = 0):
        '''
        Given container locator, identify the locator type and path from the OR file and click on the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(container)),self.locatorpath(container)).find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()
        
    # input text to web element using locatorname and value
    @fWaitFor
    def input_text(self,locator,value,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).clear()
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(value)

    @fWaitFor
    def clickandinput_text(self,locator,value,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        element= self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        #self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(value)
        element.click()
        element.send_keys(value)
        element.send_keys(Keys.ENTER)

    # Read the element text using locatorname
    @fWaitFor
    def get_text(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and return the text
        '''
        return self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).text

    # function to open a project using project name in landing page
    @fWaitFor
    def click_ProjectName(self,ProjectName,UnivWaitFor = 0):
        time.sleep(30)
        '''
        Given project name, click on the element
        '''
        # time.sleep(10)
        # element = self.driver.find_element(By.ID,"searchIcon")
        # element.click()
        # time.sleep(5)
        # element1 = self.driver.find_element(By.ID, "searchInput" )
        # element1.send_keys(str( ProjectName ))
        # element1.send_keys(Keys.ENTER)
        # time.sleep(5)
        # element2 = self.driver.find_element_by_link_text(f'{ProjectName}')
        # element2.click()

        element = self.driver.find_element(By.XPATH,"(//*[@id='root']//span[@class='ag-icon ag-icon-menu'])[1]")
        element.click()
        time.sleep(2)
        element1 = self.driver.find_element(By.XPATH,"//*[@aria-label='Filter Value']")
        element1.send_keys(str( ProjectName ))
        element1.send_keys(Keys.ENTER)
        time.sleep(5)
        element2 = self.driver.find_element_by_link_text(f'{ProjectName}')
        element2.click()

    # function to select an element
    @fWaitFor
    def select_element(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and select the element
        '''
        element = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        return element

    # functions to switch in and out of iframe on TOA page
    @fWaitFor
    def switchto(self,locator,UnivWaitFor = 0):
        '''
        Switch to a frame using locator
        '''
        iframe = self.select_element(locator,UnivWaitFor = 0)
        self.driver.switch_to.frame(iframe)
    
    @fWaitFor
    def switchout(self,UnivWaitFor = 0):
        '''
        Switch out of iframe given the iframe id
        '''
        self.driver.switch_to.default_content()

    @fWaitFor
    def timenow(self,UnivWaitFor = 0):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    @fWaitFor
    def assertPageTitle(self, pageTitle, UnivWaitFor = 0):
        '''
        Assert the title of the page
        '''
        assert self.driver.title == pageTitle

    @fWaitFor
    def numberInText(self, locator, UnivWaitFor = 0 ):
        modelCount = self.get_text(locator)
        assert any(map(str.isdigit,modelCount))
    
    @fWaitFor
    def findElementBy(self, By, locator, UnivWaitFor = 0):
        '''
        Input syntax same as of driver.find_element()
        '''
        return self.driver.find_element(By, locator)    
    
    @fWaitFor
    def getAttribute( self, locator, attribute, UnivWaitFor = 0 ):
        '''
        Input syntax same as of driver.find_element().get_attribute()
        '''
        return self.select_element( locator ).get_attribute(attribute)

    @fWaitFor
    def refreshPage( self ):
        '''
        Refreshes the page
        '''
        self.driver.refresh()

    @fWaitFor
    def compareCSV( self, actualCSV, expectedCSV, diffCSV):
        try:
            t1 = pd.read_csv(expectedCSV)
            t2 = pd.read_csv(actualCSV)
            colstbl1 = len(t1.axes[1])
            colstbl2 = len(t2.axes[1])
            if colstbl1 != colstbl2:
                return False
            else:
                result = t1.merge(t2,indicator=True,how='outer')
                finalResult = pd.DataFrame(result)
                finalResult.to_csv(diffCSV, index=False, mode='a', header=True)
                actTblMisMatchCount = finalResult['_merge'].str.contains('left_only').sum()
                expTblMisMatchCount = finalResult['_merge'].str.contains('right_only').sum()
                if actTblMisMatchCount == 0 and expTblMisMatchCount == 0:
                    return True
                else:
                    return False
        except Exception as e:
                print(e)
                
    @fWaitFor
    def selectByvisibleText(self,locator,value,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and select the dropdown value
        '''
        select = Select(self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)))
        select.select_by_visible_text(value)
    
    @fWaitFor
    def genarateRandomString(self):
        '''
        Return the dynamic string text which we can use for input text boxes
        '''
        sizeOfStr =random.randint(1, 20)
        storingstring = ''.join(random.choices(string.ascii_letters,k=sizeOfStr))
        finalRandomString = 'auto_'+str(storingstring)
        return finalRandomString
        
    @fWaitFor
    def input_text_random(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element with dynamic string
        '''
        RandomValue = self.genarateRandomString()
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).clear()
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(RandomValue)

    @fWaitFor
    def input_text_with_ctrlAltDel(self,locator,value,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element with clearing the text with control alt and delete
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.CONTROL + "a"+Keys.DELETE)
        value=str(value)
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(value)

    @fWaitFor
    def clickMultipleTimesOnElement(self,locator,noOfClicks):
        '''
        Given locator, identify the locator type and path from the OR file and click on the same element multiple times
        '''
        count = 1 
        while count <= noOfClicks:
            try:
                time.sleep(5)
                self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()
                # print("Button clicked #", count+1)
                count += 1
            except TimeoutException:
                break
    @fWaitFor
    def getdefaultselectedValueFromDropdown(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and return dropdown default value
        '''
        select = Select(self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)))
        element = select.first_selected_option.text
        return element

    @fWaitFor
    def enterTheTextDynamicallyThroughIndex(self,locator,index,value,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element on index basis
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),f'{self.locatorpath(locator)}[{index}]').send_keys(Keys.CONTROL + "a"+Keys.DELETE)
        value=str(value)
        self.driver.find_element(getattr(By,self.locatortype(locator)),f'{self.locatorpath(locator)}[{index}]').send_keys(value)

    def clickOnTheElementDynamically(self,locator,index):
        '''
        Given locator, identify the locator type and path from the OR file and click on the element dynamically  on index basis
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),f'{self.locatorpath(locator)}[{index}]').click()
    
    @fWaitFor
    def verifyelement_isdisplayed(self, locator, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the bool value
        """
        
        elementvisible = self.driver.find_element(getattr(By, self.locatortype(locator)),self.locatorpath(locator)).is_displayed()
        return elementvisible   
    
 
    @fWaitFor
    def getFirstSelectedOptionofDropdown(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and return the default dropdown value
        '''
        select = Select(self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)))
        select.first_selected_option.text


    @fWaitFor
    def verifyelement_displayed(self, locator, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the bool value
        """
        
        return self.driver.find_element(getattr(By, self.locatortype(locator)),self.locatorpath(locator)).is_displayed()
        

    #Author- Sowmya
    #This method is to clearTextbox
    @fWaitFor
    def ClearTextboxandPressTab(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        # self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()
        # self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.CONTROL + "a")
        # self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.DELETE)
        # self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.TAB)
        element = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(Keys.TAB)

    @fWaitFor
    def PressTab(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.TAB)

    #Author- Sowmya
    #This method is to clearTextbox and do not press tab
    def CtrldelTextbox(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.DELETE)
    
    #Author- Sowmya
    #This method is to clearTextbox and do not press tab
    def clickandpressTab(self,locator,UnivWaitFor = 0):
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.TAB)

    #Author- Sowmya
    #This method is to find elements under one class / one shadow
    def findsimilarElements(self,locator):
        '''
        Given locator, identify all the elements comes under that particular locator
        '''
        elenames = self.driver.find_elements(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).to_List()
        for textboxes in elenames:  
            return textboxes 
    
     #Author- Sowmya
    #Pass the 'dropdown_id' as parameter
    def ExtractDropdownItems_SelectDropdownn(self,locator,UnivWaitFor = 0):      
        dropdown_element = self.driver.find_elements(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        dropdown = Select(dropdown_element)
        dropdown_items = [option.text for option in dropdown.options]
        for item in dropdown_items:
            print(item)
            return item
        
    def get_select_dropdown_items(self, dropdown_id,UnivWaitFor=0):    
        # Locate the dropdown element using its ID
            dropdown = Select(self.driver.find_element(getattr(By,self.locatortype(dropdown_id)),self.locatorpath(dropdown_id)))
            # Get all the options from the dropdown
            options = [option.text for option in dropdown.options]
            return options

    def get_dropdown_items(self, locator,UnivWaitFor=0):
            # Wait for the dropdown to be present
            element=self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((element))            )
            # Click the dropdown to reveal its items
            dropdown.click()
            # Find all the dropdown items
            items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(f"{element} > .dropdown-item"))          
            # Extract and return the text of each item
            return [item.text for item in items]

    def ExtractDropdownItems_DynamicDropdown(self,locator,UnivWaitFor = 0):
            # Wait for the dropdown element to be visible
        dropdown_element = wait.until(EC.visibility_of_element_located((By.ID, locator)))

        # Click the dropdown element to reveal the options
        dropdown_element.click()

        # Wait for the options to be visible
        options = wait.until(EC.visibility_of_all_elements_located((By.XPATH, (locator))))

        # Extract the text values from the options
        for option in options:
            print(option.text)

    #Author- Sowmya
    #This method is to pull all the locators related to one module from OR file
    @fWaitFor
    def getlocatorModule(self,locatorname,UnivWaitFor = 0):
        df = self.read_data_from_csv(ReadConfig.getORFilePath())
        return df.loc[df['Module']==locatorname]['Object'].to_list()[0]

    @fWaitFor
    def isenabled(self, locator, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the bool value
        """
        return self.driver.find_element(getattr(By, self.locatortype(locator)),self.locatorpath(locator)).is_enabled()

    @fWaitFor
    def isdisabled(self,locator,UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the bool value
        """
        element = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).is_enabled()
        if element == False:
            return True
    
    @fWaitFor
    def is_button_disabled(self,locator,UnivWaitFor=0):
        button = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        return button.get_attribute('disabled')

    def is_button_enabled(self,locator,UnivWaitFor=0):
        button = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        return not button.get_attribute('disabled')

    def returnListOfWebelements(self,locatorForListOfElements):
        '''
        Given locator, identify all the elements comes under that particular locator
        '''
        getXpath = getattr(By,self.locatortype(locatorForListOfElements)),self.locatorpath(locatorForListOfElements)
        locator = getXpath[1]
        elenames =[]
        storingWebelementsTexts=[]
        elenames = self.driver.find_elements_by_xpath(locator)
        for elementtexts in elenames:
            storingWebelementsTexts.append(elementtexts.text)
        return storingWebelementsTexts  
    
    #Author- Sowmya
    #This method is to compare actual and expected element
    def CompareexpectedatualElement(self,actualelement,expectedelement):
        elementvisible = self.driver.find_element(getattr(By, self.locatortype(actualelement)),self.locatorpath(actualelement))
        if elementvisible == expectedelement:
            return True

    #Author- Sowmya
    #This method is to verify the text of a Textbox with expected text   
    def verifyTextboxValue(self,locator,expectedelement):
        try:
            textbox_value= self.driver.find_element(getattr(By, self.locatortype(locator)),self.locatorpath(locator))
            if textbox_value.get_attribute("value") == expectedelement:
                print(f'Textbox value is {expectedelement}')
        except Exception as e:
            
                print(f'Textbox value is not {expectedelement}')
            
    #Author- Sowmya
    #This method is to scroll down in any webpage with height mentioned in pixel
    def windowsScroll(self):
        self.driver.execute_script("window.scrollTo(0, 1000)")

    @fWaitFor
    def windowsScrolltoBottom(self):
        body = self.driver.find_element_by_tag_name('body')
        # Press the END key until reaching the bottom of the page
        while True:
        # Scroll down to the bottom of the page
            body.send_keys(Keys.END)

    #Author- Sowmya
    #This method is to accept an alert
    @fWaitFor
    def switchtoalertAccept(self):

        '''
        Switch to an alert 
        '''
        WebDriverWait(self.driver, 5).until(EC.alert_is_present(), 'Timed out waiting for alert ' )
        alert =  self.driver.switch_to.alert.accept()
        if alert == True:
            alert.accept()
            print("alert accepted")
        else:
            self.driver.switch_to.default_content()
    
    #Author- Sowmya
    #This method is to verify that element is enabled
    @fWaitFor
    def element_is_enabled(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and return the text
        '''
        return self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).is_enabled()

    @fWaitFor
    def backSpace_Keyboard(self,locator,UnivWaitFor = 0):
        '''
        Given locator, identify the locator type and path from the OR file and input text to the element
        '''
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).click()
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.BACKSPACE)

    
 
    @fWaitFor
    def check_elementnotexists_by_xpath(self,locator,UnivWaitFor=0):
        try:
            if self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).is_displayed()==True:
                print("Element is present in UI")
        except NoSuchElementException:
                pass
                print("Element is not present in UI")
    
    @fWaitFor
    def Verifyelement_not_visible(self, locator, UnivWaitFor=0):
        # try:
        #     if self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).is_displayed()==False: 
        #         print("Element is not present in UI")
        # except NoSuchElementException:
        #         print("Element is present in UI")
        locator=self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        if locator.is_displayed:
            return False
        else:
            return True
            
      

    @fWaitFor
    def Uncheck_theCheckBoxIfItIschecked(self,locator):
        element = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        actualValue = element.get_attribute('value')
        if actualValue== True:
            element.click()
            print("Check box is Unchecked")
        else:
            print("Check box is not unchecked")


    @fWaitFor
    def input_text_presstab(self,locator,value,UnivWaitFor = 0):
            '''
            Given locator, identify the locator type and path from the OR file and input text to the element with clearing the text with control alt and delete
            '''
            self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.CONTROL + "a"+Keys.DELETE)
            value=str(value)
            self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(value)
            self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).send_keys(Keys.TAB)


    def listOfWebElements(self,locatorForListOfElements):
        '''
        Provided the locator, return list of web elements and click on each element in loop
        '''
        listOfWebElements = self.driver.find_elements_by_xpath(self.locatorpath(locatorForListOfElements))

        return listOfWebElements

    
    def listOfTextWRTElements(self,webElementList):
        '''
        adding the text content from multiple web elements to the list
        '''
        textsInList = []
        for ele in webElementList:
            text = ele.text
            textsInList.append(text)
        return textsInList

    def getSimNameInDownCSVName(self):
        '''
        Gets the simulation name from simulation dropdown in TOA page
        '''
        self.switchout(UnivWaitFor=60)
        simText = self.get_text("projectSimulations_dropdown")
        print(simText)
        # self.LogScreenshot.fLogScreenshot( message = f"Switch out of iframe successful {simText} ",
        #     pass_= True, log = True, screenshot= False )
        simName = self.get_text("projectSimulations_dropdown").replace(" ","_").replace(")","").replace("(","-").split("\n")[0]
        print(simName)
        try:
            self.switchto("iframe",UnivWaitFor=60)
            # self.LogScreenshot.fLogScreenshot( message = "Switch to iframe",
            # pass_= True, log = True, screenshot= False )
        except Exception:
            # self.LogScreenshot.fLogScreenshot( message = "Switch to iframe",
            # pass_= False, log = True, screenshot= False )
            raise Exception
        return simName
    def moveToElementAndClick(self,locatorToBeMove,locatorToBeClick):
        '''
        this method will do mouse over menu and click on particular element
        '''
        action = ActionChains(self.driver)
        element = self.select_element(locatorToBeMove)
        action.move_to_element(element).perform()
        self.driver.find_element(getattr(By,self.locatortype(locatorToBeClick)),self.locatorpath(locatorToBeClick)).click()

    def findElements(self,locator):
        '''
        This method will return the group of elements
        '''
        elements = self.driver.find_elements(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        return elements
    
    def findElement(self,locator):
        '''
        This method will return the group of elements
        '''
        element = self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator))
        return element
       

    def enter_text_in_textbox_using_js(self,locator,text):
      # Execute the JavaScript function to enter text in the textbox      
        self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).clear()
        self.driver.execute_script(f'enterTextInTextbox("{text}")')

    def PressEnterKey(self,locator,UnivWaitFor=0):
      # Execute the JavaScript function to enter text in the textbox      
        element=self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)).clear()
        element.send_keys(Keys.ENTER)

    def ExtractDropdownItems_SelectDropdown(self,locator,UnivWaitFor = 0):
                
        select_element = Select(self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)))
        all_options=[option.text.strip() for option in select_element.options]
        return all_options
    
    def CompareActualDropdownItems_toExpectedlist(self,locator,expected_items,UnivWaitFor = 0):
        select_element = Select(self.driver.find_element(getattr(By,self.locatortype(locator)),self.locatorpath(locator)))
        all_options = select_element.options    
        actual_items = [option.text for option in all_options]
        if actual_items == expected_items:
            return True
        
    def getTheUpdatedXpath(self,locatorForListOfElements,index):
        '''
        This method will return the updated xpath based on index and locator .
        '''
        getXpath = getattr(By,self.locatortype(locatorForListOfElements)),self.locatorpath(locatorForListOfElements)
        index=str(index)
        locator = getXpath[1].replace("index",index)
        return locator
    
    
    def get_CurrentURL(self):
        return self.driver.current_url
        

    