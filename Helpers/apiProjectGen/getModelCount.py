import requests
import datetime

##############################################################################################
#### Get Model Count
def getModelCount(authData,hashkey,access_token,expModels,userPortalDetails,projectGen):
    req_urlGetMC = authData['BaseUrl'] +"/"+ authData['SimUrl'] +"/"+ "simulation/modelcount/" + str(userPortalDetails['ResourceID']) +"/" + str(projectGen['ProjectID'])
    # number of models info will be passed to the create project function directly.
    # noOfModelExpected = str(objectData["ExpectedModels"][i])

    headersGetMC = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    responseGetMC = requests.get(req_urlGetMC, headers=headersGetMC)
    jsonResponseGetMC = responseGetMC.json()
    if responseGetMC.status_code == 200:
        noOfModelFromNewlyCreatedProject = str(jsonResponseGetMC["noOfModels"])
        if (expModels == noOfModelFromNewlyCreatedProject):
            print(str(datetime.datetime.now()) + " : #Models From Newly Created Project are matching with #Model Expected i.e. " + str(noOfModelFromNewlyCreatedProject))
        elif (expModels != noOfModelFromNewlyCreatedProject):
            print(str(datetime.datetime.now()) + " : #Models From Newly Created Project " + str(noOfModelFromNewlyCreatedProject) + " NOT matching with #Model Expected " + str(expModels))
        else:
            raise Exception("Either or both expected model or actual model count is an invalid field")
    else:
        print(str(datetime.datetime.now()) + " : Get model count failed with an error " + str(responseGetMC.status_code))
        raise Exception("Get model count failed with an error " + str(responseGetMC.status_code))