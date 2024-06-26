import requests
import datetime
import json

def createSimulation(authData,hashkey,access_token,userPortalDetails,projectGen):

    req_urlCreateSimulation = authData['BaseUrl'] +"/"+ authData['SimUrl'] +"/"+ "simulation/create"
    headersCreateSimulation = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }

    dataCreateSimulation = {
    'projectId': int(projectGen['ProjectID']),
    'resourceId': int(userPortalDetails['ResourceID']),
    'clientId': int(authData['securityGroupID']),
    'createdBy': authData['username'],
    'entitlementID': userPortalDetails['clientEntitlementID'],
    'portalTenantID': userPortalDetails['portalTenantID'],
    'portalUserID': authData['portalUserID'],
    }

    responseCreateSimulation = requests.post(req_urlCreateSimulation, headers=headersCreateSimulation, data=json.dumps(dataCreateSimulation))
    jsonResponseCreateSimulation = responseCreateSimulation.json()

    if responseCreateSimulation.status_code == 200:
        createSimulation = {
            'projectSimulationID' : str(jsonResponseCreateSimulation["projectSimulationID"]),
            'noOfModels' : str(jsonResponseCreateSimulation["noOfModels"]),
            'endpointType' : str(jsonResponseCreateSimulation["endpointType"]),
            'numberOfSimulationRun' : str(jsonResponseCreateSimulation["numberOfSimulationRun"]),
        }
        print(str(datetime.datetime.now()) + " : Simulation created successfully for Project Simulation Id: " + createSimulation['projectSimulationID'] + "  for #Models: "+ createSimulation['noOfModels'] + " Endpoint Type: " + createSimulation['endpointType'] + " #SimusPerModel: " + createSimulation['numberOfSimulationRun'])
    else:
        print(str(datetime.datetime.now()) + " : Simulation Creation failed with an error " + str(responseCreateSimulation.status_code))
        raise Exception("Simulation Creation failed with an error " + str(responseCreateSimulation.status_code))

    return createSimulation
    