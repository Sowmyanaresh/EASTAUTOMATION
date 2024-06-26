import requests
import json

def loadInputJson(authData,hashkey,access_token,readJson,userPortalDetails,projectGen):
    req_urlLoadIA = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] +"/"+ "inputadvisor/'plans'"
    headersLoadIA = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataLoadIA = {
            "object" : readJson['iajson'],
            "createdBy": authData['username'],
            "projectID": projectGen['ProjectID'],
            "resourceID": userPortalDetails['ResourceID']        

    }
    responseLoadIA = requests.post(req_urlLoadIA, headers=headersLoadIA, data=json.dumps(dataLoadIA))
    jsonResponseLoadIA = responseLoadIA.json()
 
    if responseLoadIA.status_code == 201:
        loadInputJson = {
            'aProjectID' : str(jsonResponseLoadIA["projectID"]),
            'InputAdvID' : str(jsonResponseLoadIA["inputAdvisorID"])
        }
        
        print("Input Advisor Data created successfully for Project ID " + loadInputJson['aProjectID'] + "  and Input Advisor Id is "+ loadInputJson['InputAdvID'])
    else:
        print("Input Advisor Data creation failed with an error " + str(responseLoadIA.status_code))
        raise Exception("Input Advisor Data creation failed with an error " + str(responseLoadIA.status_code))

    print(f'{readJson["json_file"]} project created!')

