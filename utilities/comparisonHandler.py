import time
from Helpers.Base import Base
import os
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot

class cComparisonHandler:
    def __init__(self, driver, extra):
        self.driver = driver
        self.base = Base(self.driver)
        self.LogScreenshot = cLogScreenshot(self.driver,extra)

    def compareFiles( self, fileType, file1Name, file1Location, file2Name, file2Location):
        '''
        Precondition: The files to be compared should be in their respective folders
        Purpose: Compare the two files and return the result
        Input:
        1. fileType: The file type of the files to be compared. eg., csv, png, etc.
        2. file1Name: The name of the first file to be compared
        3. file1Location: The location of the first file to be compared
        4. file2Name: The name of the second file to be compared
        5. file2Location: The location of the second file to be compared
        '''
        # read the files
        file1 = open(f'{file1Location}/{file1Name}', 'r')
        file2 = open(f'{file2Location}/{file2Name}', 'r')
        file1Lines = file1.readlines()
        file2Lines = file2.readlines()
        file1.close()
        file2.close()
        
        # compare the files
        if len(file1Lines) != len(file2Lines):
            return False
        else:
            for i in range(len(file1Lines)):
                if file1Lines[i] != file2Lines[i]:
                    return False
            return True