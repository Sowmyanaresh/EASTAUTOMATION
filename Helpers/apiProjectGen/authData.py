from utilities.readProperties import ReadConfig

def authData(environmentType = 'test',environment = 'test5'):
    '''
    input:
    enviornmentType: Takes value either 'test' or 'beta'
    environment: Takes value like 'test1', 'test2' if environmentType is 'test' and 'beta', 'beta2' if environmentType is 'beta'
    output:
    Returns a dictionary with all the values required for authentication
    '''
    if environmentType == 'test':
        ## test environment
        authData = {
        'req_urlGenToken' : 'https://cytel.oktapreview.com/oauth2/default/v1/token',
        'cHost' : 'cytel.oktapreview.com',
        'client_id' : ReadConfig.getAuthInput("clientID"),
        'scope' : 'user.read.all transaction.readwrite tenant.read.all',
        'client_secret' : ReadConfig.getAuthInput("clientSecret"),
        'BaseUrl' : "https://dev-apis.cytel.com",
        'PrjMgrUrl' : f"solara-projectmgr-{environment}/v1/api/v1.0",
        'SimUrl' : f'solara-simulation-{environment}/v1/api/v1.0',
        'QueryUrl' : f'solara-query-{environment}/v1/api/v1.0',
        'portalUserID' : ReadConfig.getAuthInput("portalUserID"),
        'securityGroupID' : ReadConfig.getAuthInput("securityGroupID"),
        'username'  : ReadConfig.getAuthInput("app_username"),
        'password' : ReadConfig.getPassword(),
        'cyt_api_key' : ReadConfig.getAuthInput("cyt_api_key"),
        'hashkey' :ReadConfig.getAuthInput("hashkey"),
        'grant_type' : 'password',
        'cType' : 'application/x-www-form-urlencoded',
        'cLen' : b'239',
        }
    elif environmentType == 'beta':
        ## beta environment
        authData = {
        'req_urlGenToken' : 'https://cytel.okta.com/oauth2/default/v1/token',
        'cHost' : 'cytel.okta.com',
        'client_id' : ReadConfig.getAuthInput("clientID"),
        'scope' : 'user.read.all transaction.readwrite tenant.read.all',
        'client_secret' : ReadConfig.getAuthInput("clientSecret"),
        'BaseUrl' : "https://stg-apis.cytel.com",
        'PrjMgrUrl' : f"solara-projectmgr-stg-{environment}2/v1/api/v1.0",
        'SimUrl' : f'solara-simulation-stg-{environment}2/v1/api/v1.0',
        'QueryUrl' : f'solara-query-stg-{environment}2/v1/api/v1.0',    
        'portalUserID' : ReadConfig.getAuthInput("portalUserID"),
        'securityGroupID' : ReadConfig.getAuthInput("securityGroupID"),
        'username'  : ReadConfig.getAuthInput("app_username"),
        'password' : ReadConfig.getPassword(),
        'cyt_api_key' : ReadConfig.getAuthInput("cyt_api_key"),
        'hashkey' :ReadConfig.getAuthInput("hashkey"),
        'grant_type' : 'password',
        'cType' : 'application/x-www-form-urlencoded',
        'cLen' : b'239'
        }
    else: 
        print("Provide correct value for environment and environment type")
        raise Exception("Provide correct value for environment and environment type")
    return authData