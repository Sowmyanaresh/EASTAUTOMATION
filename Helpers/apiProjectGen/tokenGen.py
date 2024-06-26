################################################################################################################################################################
#### Token generation
import requests
import datetime
from utilities.readProperties import ReadConfig

def tokenGen(authData):

    headersAPI = {
        'Content-Type': authData['cType'],
        'Content-Length': authData['cLen'],
        'Host': authData['cHost']
    }
    data = {
            'client_id': authData['client_id'],
            'scope': authData['scope'],
            'client_secret': authData['client_secret'],
            'grant_type': authData['grant_type'],
            'username': authData['username'],
            'password': authData['password']
    }
    ## Authentication request
    response = requests.post(authData['req_urlGenToken'], headers=headersAPI, data=data)
    tknjsonResponse = response.json()

    if response.status_code == 200:
        access_token = "Bearer " + str(tknjsonResponse["access_token"])
        print(str(datetime.datetime.now()) + " : Token generated successfully " )#+ access_token)
    else:
        print(str(datetime.datetime.now()) + " : Token generation failed with an error " + str(tknjsonResponse['status_code']))
        raise Exception("Token generation failed with an error " + str(tknjsonResponse['status_code']))

    tokenGen = {'access_token':access_token,
    }
    return tokenGen
