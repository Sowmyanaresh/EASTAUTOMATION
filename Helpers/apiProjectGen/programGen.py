import requests
import json
import string
import random

def programGen(authData,hashkey,access_token,userPortalDetails):
    req_urlProgram = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] +"/"+ "programs"
    letters = string.ascii_uppercase
    ProgramName = "AutoPgrm_" + str(''.join(random.choice(letters) for i in range(4)))
    headersProgramAPI = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataPgrm = {
            'programName': ProgramName, 
            'resourceID': userPortalDetails['ResourceID'], 
            'createdBy': authData['username']
    }
    responsePgrm = requests.post(req_urlProgram, headers=headersProgramAPI, data=json.dumps(dataPgrm))
    jsonResponsePgrm = responsePgrm.json()
    if responsePgrm.status_code == 201:
        programGen = {
            'ProgramID' : str(jsonResponsePgrm["id"]),
            'ProgramName' : str(jsonResponsePgrm["name"])
        }
        print("Program created successfully with Id as " + programGen['ProgramID'] + "  and Name as "+programGen['ProgramName'])
    else:
        print("Program creation failed with an error " + str(responsePgrm.status_code))
        raise Exception("Program creation failed with an error " + str(responsePgrm.status_code))
    return programGen