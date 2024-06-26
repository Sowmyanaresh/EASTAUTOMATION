import requests
import string
import random
import json

def indicationGen(authData,hashkey,access_token,userPortalDetails):
    req_urlIndication = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] +"/"+ "indications"
    letters = string.ascii_uppercase
    IndicationName = "AutoInd_" + str(''.join(random.choice(letters) for i in range(4)))
    headersIndicationAPI = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataInd = {
            'indicationName': IndicationName, 
            'resourceID': userPortalDetails['ResourceID'], 
            'createdBy': authData['username']
    }
    responseInd = requests.post(req_urlIndication, headers=headersIndicationAPI, data=json.dumps(dataInd))
    jsonResponseInd = responseInd.json()
    
    if responseInd.status_code == 201:
        indicationGen = {
            'IndicationID' : str(jsonResponseInd["id"]),
            'IndicationName' : str(jsonResponseInd["value"])
        }
        print("Indication created successfully with Id as " + indicationGen['IndicationID'] + "  and Name as "+ indicationGen['IndicationName'])
    else:
        print("Indication creation failed with an error " + str(responseInd.status_code))
        raise Exception("Indication creation failed with an error " + str(responseInd.status_code))
    return indicationGen