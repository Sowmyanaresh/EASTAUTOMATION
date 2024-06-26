import time
from Helpers.Base import Base
import os
from utilities.customLogger import LogGen
from utilities.logScreenshot import cLogScreenshot

class cDownloadHandler:
    def __init__(self, driver, extra):
        self.driver = driver
        self.base = Base(self.driver)
        self.LogScreenshot = cLogScreenshot(self.driver,extra)

    def nameFile( self, fileType, testSuite, projectName, stepName, testRun = 'actual' ):
        '''
        Inputs:
        1. fileType = file type extension. eg., csv, png,etc
        2. testSuite = name of the testsuite being run. eg., if test_smoke.py is run, then test suite is smoke
        3. projectName = name of the project which is open in toa currently
        4. stepName = name of the step after which to download/save and name the file
        5. testRun = whether the file is saved as 'benchmark' or 'actual'. can only take these two values.
        Output: file name with extension
        '''
        if testRun == 'actual':
            return f'{testSuite}_{projectName}_{stepName}_{self.base.timenow()}.{fileType}'
        elif testRun == 'benchmark':
            return f'{testSuite}_{projectName}_{stepName}_benchmark.{fileType}'
        else:
            raise Exception(f'Invalid testRunType: {testRun}')       
        

    def moveAndRename( self, downloadFunc, fileType, renameTo, moveTo, testRunType = 'actual', waitTime = 20 ):
        '''
        Precondition: A file download action should be performed on chrome before using this function
        Purpose: Move the last downloaded file on chrome to the specified folder and rename it.
        Input:
        1. downloadFunc: The function that performs the download action.
        2. filetype: The file type of the downloaded file. eg., csv, png, etc.
        3. renameTo: The new name of the file exluding extension. 
            a. timestamp or the string 'benchmark' will be appended to this name based on the value in testRunType
            b. extension will be appended to this name based on the value in filetype
        4. moveTo: The folder where the file is to be moved to
            a. Relative to the 'ActualOutputs' or 'Testdata/Benchmarks' folder based on the value in testRunType
        5. testRunType: The type of test run. Can only take two values: actual or benchmark
        6. waitTime: The time in seconds to wait for the file to be downloaded
        '''
        # remove all files with fileType extension in the download folder
        allFiles = os.listdir("ActualOutputs")
        for item in allFiles:
            if item.endswith(f".{fileType}"):
                os.remove("ActualOutputs/" + item)

        # download the file
        try:
            downloadFunc()
        except Exception as e:
            raise e

        # read downloaded file name. if the file is not downloaded, wait for the specified time
        endTime = time.time() + waitTime
        onlyfileTypeFiles = [f for f in os.listdir("ActualOutputs") if f.endswith(f".{fileType}")]
        while len(onlyfileTypeFiles) == 0:
            time.sleep(1)
            onlyfileTypeFiles = [f for f in os.listdir("ActualOutputs") if f.endswith(f".{fileType}")]
            if time.time() > endTime:
                raise Exception(f"File with {fileType} extension not downloaded in {waitTime} seconds")
        downloadedFileName = onlyfileTypeFiles[0]

        if testRunType == 'actual':
            rootFolder = 'ActualOutputs'
        elif testRunType == 'benchmark':
            rootFolder = 'Testdata/Benchmarks'
        else:
            raise Exception(f'Invalid testRunType: {testRunType}')
        
        # if the renamed file already exists in the destination folder, delete it
        if os.path.exists(f'{rootFolder}/{moveTo}/{renameTo}'):
            os.remove(f'{rootFolder}/{moveTo}/{renameTo}')

        # rename and move the file
        os.rename(f'ActualOutputs/{downloadedFileName}', f'{rootFolder}/{moveTo}/{renameTo}')

    def saveFile( self, fileToSave, saveAs, saveLocation, fileType = 'csv', testRunType = 'actual' ):
        '''
        Input:
        1. fileType - type of file. eg., 'csv','png',etc. Currently only 'csv' writing feature available
        2. saveAs - name of the file to be saved. eg., 'test_smoke_test_1_benchmark.csv'
        3. saveLocation - location where the file is to be saved relative to 'ActualOutputs' or 'Testdata/Benchmarks'. 
            eg., tableViewOutputs
        4. testRunType - whether the file is saved as 'actual' or 'benchmark'
        '''
        if testRunType == 'actual':
            rootFolder = 'ActualOutputs'
        elif testRunType == 'benchmark':
            rootFolder = 'Testdata/Benchmarks'
        else:
            raise Exception(f'Invalid testRunType: {testRunType}')

        if fileType == 'csv':
            fileToSave.to_csv( f'{rootFolder}/{saveLocation}/{saveAs}', index=False )
        else:
            raise Exception(f'Invalid fileType: {fileType}')
        
