from Helpers.apiProjectGen import authData
from Helpers.apiProjectGen import tokenGen
from Helpers.apiProjectGen import hashkeyGen
from Helpers.apiProjectGen import readJson
from Helpers.apiProjectGen import userPortalDetails
from Helpers.apiProjectGen import indicationGen
from Helpers.apiProjectGen import programGen
from Helpers.apiProjectGen import projectGen
from Helpers.apiProjectGen import loadInputJson
from Helpers.apiProjectGen import getModelCount
from Helpers.apiProjectGen import createSimulation
from Helpers.apiProjectGen import submitSimulation
from Helpers.apiProjectGen import checkProgress
import pandas as pd
import time
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen

class cCreateProject:

    sJsonDir = ".//TestData//inputJsons"
    senvironmentType = ReadConfig.getEnvironmenttype()
    senvironment = ReadConfig.getEnvironment()

    logger = LogGen.loggen()

    def fCreateProject(self,IAjson,expModels,waitfor,ProjectName):
        '''
        IAjson: Input Json file name for the project
        expModels: Expected number of models for the project
        waitfor: maximum waiting period for the project to be simulated before failing the test case
        ProjectName: Name of the project
        '''
        time.sleep(1)
        # Read authentication data
        try:
            dauthData = authData.authData(self.senvironmentType,self.senvironment)
            self.logger.info("PASS: Read authentication data")
        except:
            self.logger.error("FAIL: Read authentication data")
            raise Exception("FAIL: Read authentication data")
        
        # Generate token
        try:
            dtokenGen = tokenGen.tokenGen(dauthData)
            self.logger.info("PASS: Generated token")
        except:
            self.logger.error("FAIL: Token generation failed")
            raise Exception("FAIL: Token generation failed")

        # Generate hashkey
        try:
            hashkeyGen.hashkeyGen(dauthData,dtokenGen)
            self.logger.info("PASS: Generated hashkey")
        except:
            self.logger.error("FAIL: Hashkey generation failed")
            raise Exception("Hashkey generation failed")

        # Read input json
        try:
            dreadJson = readJson.readJson(IAjson=IAjson,jsonDir=self.sJsonDir)
            self.logger.info("PASS: Read input json")
        except:
            self.logger.error("FAIL: Read input json failed")
            raise Exception("FAIL: Read input json failed")

        # Read user portal details
        try:
            duserPortalDetails = userPortalDetails.userPortalDetails(dauthData,dauthData["hashkey"],dtokenGen["access_token"])
            self.logger.info("PASS: Read user portal details")
        except:
            self.logger.error("FAIL: Read user portal details failed")
            raise Exception("FAIL: Read user portal details failed")
        
        # Generate indication
        try:
            dindicationGen = indicationGen.indicationGen(dauthData,dauthData["hashkey"],dtokenGen["access_token"],duserPortalDetails)
            self.logger.info("PASS: Generated indication")
        except:
            self.logger.error("FAIL: Indication generation failed")
            raise Exception("FAIL: Indication generation failed")

        # Generate program
        try:
            dprogramGen = programGen.programGen(dauthData,dauthData["hashkey"],dtokenGen["access_token"],duserPortalDetails)
            self.logger.info("PASS: Generated program")
        except:
            self.logger.error("FAIL: Program generation failed")
            raise Exception("FAIL: Program generation failed")

        # Generate project
        try:
            dprojectGen = projectGen.projectGen(dauthData,dauthData["hashkey"],dtokenGen["access_token"],dreadJson,duserPortalDetails,dindicationGen,dprogramGen,ProjectName)
            self.logger.info("PASS: Generated project")
        except:
            self.logger.error("FAIL: Project generation failed")
            raise Exception("FAIL: Project generation failed")

        # Load input json
        try:
            loadInputJson.loadInputJson(dauthData,dauthData["hashkey"],dtokenGen["access_token"],dreadJson,duserPortalDetails,dprojectGen)
            self.logger.info("PASS: Loaded input json")
        except:
            self.logger.error("FAIL: Loading input json failed")
            raise Exception("FAIL: Loading input json failed")

        # Get model count
        try:
            getModelCount.getModelCount(dauthData,dauthData["hashkey"],dtokenGen["access_token"],expModels,duserPortalDetails,dprojectGen)
            self.logger.info("PASS: Got model count")
        except:
            self.logger.error("FAIL: Getting model count failed")
            # raise Exception("FAIL: Getting model count failed")

        # Create simulation
        try:
            dcreateSimulation = createSimulation.createSimulation(dauthData,dauthData["hashkey"],dtokenGen["access_token"],duserPortalDetails,dprojectGen)
            self.logger.info("PASS: Created simulation")
        except:
            self.logger.error("FAIL: Simulation creation failed")
            raise Exception("FAIL: Simulation creation failed")
        
        # Submit simulation
        try:
            submitSimulation.submitSimulation(dauthData,dauthData["hashkey"],dtokenGen["access_token"],duserPortalDetails,dprojectGen,dcreateSimulation)
            self.logger.info("PASS: Submitted simulation")
        except:
            self.logger.error("FAIL: Simulation submission failed")
            raise Exception("FAIL: Simulation submission failed")
        
        # Check progress
        try:
            checkProgress.checkProgress(waitfor,dauthData,dauthData["hashkey"],dtokenGen["access_token"],duserPortalDetails,dprojectGen,dcreateSimulation)
            self.logger.info("PASS: Checked progress")
        except:
            self.logger.error("FAIL: Checking progress failed")
            raise Exception("FAIL: Checking progress failed")