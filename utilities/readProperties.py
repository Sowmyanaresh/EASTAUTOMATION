import configparser

config = configparser.RawConfigParser()
config.read(".\\Configurations\\config.ini")

class ReadConfig():

    # static method helps you read the function in another file without instantiating the class
    @staticmethod
    def getApplicationURL():
        env = config.get('commonInfo','environment')
        return f"https://solara-{env}.cytel.com/"

    @staticmethod
    def getUserName():
        username = config.get('commonInfo','username')
        return username

    @staticmethod
    def getPassword():
        password = config.get('commonInfo','password')
        return password

    # only used for default visual. for future development only using getwrapperTD instead
    @staticmethod
    def getwrapperTestData():
        wrapperTestData = config.get('commonInfo','defaultVisualWrapperTD')
        return wrapperTestData
    
    @staticmethod
    def getwrapperTD( wrapperfile ):
        wrapperTestData = config.get('commonInfo',wrapperfile)
        return wrapperTestData

    @staticmethod
    def getORFilePath():
        OR = config.get('commonInfo','OR')
        return OR

    @staticmethod
    def getEnvironmenttype():
        environmenttype = config.get('commonInfo','environmenttype')
        return environmenttype

    @staticmethod
    def getEnvironment():
        environment = config.get('commonInfo','environment')
        return environment

    # Read input advisor authentication data from config.ini
    @staticmethod
    def getAuthInput(authinput):
        input = config.get(ReadConfig.getEnvironmenttype(),authinput)
        return input

    @staticmethod
    def testRunType():
        testRunType = config.get('commonInfo','testRunType')
        return testRunType
    
    @staticmethod
    def projectExists():
        projectExists = config.get('commonInfo','projectExists')
        return projectExists

    @staticmethod
    def ifHeadlessMode():
        ifHeadlessMode = config.get('commonInfo','ifHeadlessMode')
        return ifHeadlessMode