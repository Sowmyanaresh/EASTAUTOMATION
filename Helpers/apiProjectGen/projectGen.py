import requests
import string
import datetime
import json

def projectGen(authData,hashkey,access_token,readJson,userPortalDetails,indicationGen,programGen,ProjectName):
    req_urlProject = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] +"/"+ "projects"
    letters = string.ascii_uppercase
    timenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ProjectName = ProjectName
    # ProjectName = f'{readJson["json_file"]}_{timenow}'
    headersProjectAPI = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    dataPrj = {
            'projectName': ProjectName, 
            'protocolID': ProjectName,
            'programID': programGen['ProgramID'],
            'indicationID': indicationGen['IndicationID'],
            'timeUnitID': 3,
            'currencyID': 3,
            'createdBy': authData['username'],
            'resourceID': userPortalDetails['ResourceID'], 
            'startDate': '11-May-2021',
            'filter':'UnArchive',
            'searchFilter':'',
            'securityGroupId': authData['securityGroupID'],
            'userFilter':''
    }
    responsePrj = requests.post(req_urlProject, headers=headersProjectAPI, data=json.dumps(dataPrj))
    jsonResponsePrj = responsePrj.json()
    projectGen ={}
    if responsePrj.status_code == 201:
        projectGen = {
            'ProjectID' : str(jsonResponsePrj["id"]),
            'ProjectName' : str(jsonResponsePrj["name"])
        }
        print("Project created successfully with Id as " + projectGen['ProjectID'] + "  and Name as "+ ProjectName)
    else:
        print("Project creation failed with an error " + str(responsePrj.status_code))
        raise Exception("Project creation failed with an error " + str(responsePrj.status_code))
    return projectGen