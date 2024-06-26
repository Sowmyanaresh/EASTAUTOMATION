import requests

def userPortalDetails(authData,hashkey,access_token):
    req_urlGetUsersPortalDetails = authData['BaseUrl'] +"/"+ authData['PrjMgrUrl'] + "/Login/GetUserInfo/" + str(authData['username']) +"/"+ str(authData['portalUserID'])
    headersGetUsersPortalDetails = {
        'cyt-api-key': authData['cyt_api_key'],
        'hashkey': hashkey,
        'username': authData['username'],
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    responseGetUsersPortalDetails = requests.get(req_urlGetUsersPortalDetails, headers=headersGetUsersPortalDetails)
    jsonResponseGetUsersPortalDetails = responseGetUsersPortalDetails.json()
    
    userPortalDetails = {}
    if responseGetUsersPortalDetails.status_code == 200:
        userPortalDetails ={
            'ResourceID' : str(jsonResponseGetUsersPortalDetails["id"]),
            'clientID' : str(jsonResponseGetUsersPortalDetails["clientID"]),
            'clientEntitlementID' : str(jsonResponseGetUsersPortalDetails["clientEntitlementID"]),
            'portalTenantID' : str(jsonResponseGetUsersPortalDetails["portalTenantID"]),
            'maxCreditPerBatch' : str(jsonResponseGetUsersPortalDetails["maxCreditPerBatch"])
        }
        print("Get Users Portal Details portalUserID " + authData['portalUserID'] + "  clientID as "+ userPortalDetails['clientID'] + "  ResourceID as "+ userPortalDetails['ResourceID'] + "  clientEntitlementID as "+ userPortalDetails['clientEntitlementID'] + "  portalTenantID as "+ userPortalDetails['portalTenantID'] + "  maxCreditPerBatch as "+ userPortalDetails['maxCreditPerBatch'])
    else:
        print("Get Users Portal Details failed with an error " + str(responseGetUsersPortalDetails.status_code))
        raise Exception("Get Users Portal Details failed with an error " + str(responseGetUsersPortalDetails.status_code))
    return userPortalDetails