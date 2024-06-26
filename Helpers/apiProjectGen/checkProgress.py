import requests
import json
import datetime
import time

def checkProgress(waitfor,authData,hashkey,access_token,userPortalDetails,ProjectGen,createSimulation):
    ##############################################################################################
    #### Check Simulation Progress
    req_urlCheckProgress = authData['BaseUrl'] +"/"+ authData['SimUrl'] +"/"+ "simulation/progress/" + str(ProjectGen['ProjectID'])
    # print(req_urlCheckProgress)
    headersCheckProgress = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataCheckProgress = {
    'projectId': int(ProjectGen['ProjectID']),
    'resourceId': userPortalDetails['ResourceID'],
    'clientId': authData['securityGroupID'],
    'createdBy': authData['username'],
    'entitlementID': userPortalDetails['clientEntitlementID'],
    'portalTenantID': userPortalDetails['portalTenantID'],
    'portalUserID': authData['portalUserID'],
    'projectSimulationId': int(createSimulation['projectSimulationID'])
    }
    # print(headersCheckProgress)
    responseCheckProgress = requests.get(req_urlCheckProgress, headers=headersCheckProgress)
    jsonResponseCheckProgress = responseCheckProgress.json()
    print(str(datetime.datetime.now()) + " : Waiting for simulation to be completed..")
    if responseCheckProgress.status_code == 200:
        j = 0
        while ((jsonResponseCheckProgress["isSimulationCompleted"] == False) and (jsonResponseCheckProgress["isSimulationCanceled"] == False)):
            time.sleep(30) #wait for 10 seconds before retrying
            j = j+1
            responseCheckProgress = requests.get(req_urlCheckProgress, headers=headersCheckProgress)
            if responseCheckProgress.status_code == 200 and j < 6*waitfor:
                jsonResponseCheckProgress = responseCheckProgress.json()
            elif responseCheckProgress.status_code == 200 and j > 6*waitfor:
                raise Exception(str(datetime.datetime.now()) + " : Simulation is taking longer than expected..")
            else:
                raise Exception("Simulation submitted failed with an error " + str(responseCheckProgress.status_code))

        # Throw an error if results aren't available 
        if jsonResponseCheckProgress["isSimulationCompleted"] == True:
            print(str(datetime.datetime.now()) +": Simulation Completed successfully")
        else:
            raise Exception("Simulation failed with an error " + str(responseCheckProgress.status_code))
        