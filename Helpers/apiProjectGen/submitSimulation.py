import requests
import json
import datetime

def submitSimulation(authData,hashkey,access_token,userPortalDetails,ProjectGen,createSimulation):
##############################################################################################
    #### Submit Simulation
    req_urlSubmitSimulation = authData['BaseUrl'] +"/"+ authData['SimUrl'] +"/"+ "simulation/submit"
    headersSubmitSimulation = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataSubmitSimulation = {
    'projectId': int(ProjectGen['ProjectID']),
    'resourceId': int(userPortalDetails['ResourceID']),
    'clientId': int(authData['securityGroupID']),
    'createdBy': authData['username'],
    'entitlementID': userPortalDetails['clientEntitlementID'],
    'portalTenantID': userPortalDetails['portalTenantID'],
    'portalUserID': authData['portalUserID'],
    'projectSimulationId': int(createSimulation['projectSimulationID']),
    }

    responseSubmitSimulation = requests.post(req_urlSubmitSimulation, headers=headersSubmitSimulation, data=json.dumps(dataSubmitSimulation))
    jsonResponseSubmitSimulation = responseSubmitSimulation.json()
    if responseSubmitSimulation.status_code == 200:
        submitted = str(jsonResponseSubmitSimulation)
        if submitted == "True":
            print(str(datetime.datetime.now()) + " : Simulation submitted successfully ")
    else:
        print(str(datetime.datetime.now()) + " : Simulation submitted failed with an error " + str(responseSubmitSimulation.status_code))
        raise Exception("Simulation submitted failed with an error " + str(responseSubmitSimulation.status_code))