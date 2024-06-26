import requests
import json
import datetime
        ##############################################################################################
        #### Hashkey generation
def hashkeyGen(authData,tokenGen):
    req_urlGenHashkey = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] +"/"+ "Login/UpdateUserSession"
    headersHashAPI = {
        'cyt-api-key': authData['cyt_api_key'],
        'username': authData['username'],
        'Authorization': tokenGen['access_token'],
        'Content-type': 'application/json'
    }
    data = {
        "UserName": authData['username'],
        "hashKey": authData['hashkey']
        }
    responseHash = requests.post(req_urlGenHashkey, headers=headersHashAPI,data=json.dumps(data))
    
    if '200' in str(responseHash.status_code):
        print(str(datetime.datetime.now()) + " : Hashkey generated successfully ")
    else:
        print(str(datetime.datetime.now()) + " : Hashkey generation failed with an error " + str(responseHash.status_code))
        raise Exception("Hashkey generation failed with an error " + str(responseHash.status_code))