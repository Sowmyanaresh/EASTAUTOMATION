import requests
import json
import datetime

import psycopg2
import pandas.io.sql as psql
#import config
import json

import pyodbc

def downloadRawCSVAzureSP(authData,ProjectSimID):                    
    server = authData['azureServer']
    database = authData['azureDatabase']
    username = authData['azureUsername']
    password = authData['azurePassword']
    dbUser = authData['dbUsername']
    dbPassword = authData['dbPassword']

    try:
                               
        # prerequisite - get the ip address approved
        ProjectSimID = 29974
        ProjectName = 'MultiArmHochberg'
        test_env = 'test6'

        # host = "psql-11-dev-cyt-solaris-eastus.postgres.database.azure.com"
        host = 'psql-dev-cyt-solara-eastus.postgres.database.azure.com'
        dbname = f'solara_{test_env}'

        connection = psycopg2.connect(host = host, dbname= dbname, user=dbUser, password=dbPassword, sslmode='verify-full', sslrootcert='BaltimoreCyberTrustRoot.crt.pem')
        dataframe = psql.read_sql(f'SELECT * FROM result."SimModelResultDataLakeSettings"  WHERE "ProjectSimulationID" = {ProjectSimID} ORDER BY "ID" DESC', connection)
        
        print(dataframe)
        print(dataframe.columns)

        # with open(f'exported_json/ProjectID_{test_env}_{ProjectSimID}_{ProjectName}.json', 'w', encoding='utf-8') as f:
        #     json.dump(dataframe['Object'][0], f, ensure_ascii=False, indent=4)
        
                
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        cursor.execute("SELECT @@VERSION as version")

        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()
            # Prepare the stored procedure execution script and parameter values
        storedProc = "Exec [ReadFile].[Mtb_GetCustomers] @SearchText = ?, @MaximumRowsToReturn = ?"
        params = ("And", 10)    

    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc, params )
    
        # Iterate the cursor
        row = cursor.fetchone()
        while row:
            # Print the row
            print(str(row[0]) + " : " + str(row[1] or '') )
            row = cursor.fetchone()
    
        # Close the cursor and delete it
        cursor.close()
        del cursor
    
        # Close the database connection
        cnxn.close()
    except Exception as e:
        print("Error: %s" % e)






# def downloadRawCSVAzureSP(authData,hashkey,access_token,userPortalDetails,ProjectGen,createSimulation):
##############################################################################################
    # ### Submit Simulation
    # req_urlSubmitSimulation = authData['BaseUrl'] +"/"+ authData['SimUrl'] +"/"+ "simulation/submit"
    # headersSubmitSimulation = {
    #     'cyt-api-key': authData['cyt_api_key'],
    #     'hashkey': hashkey,
    #     'username': authData['username'],
    #     'Authorization': access_token,
    #     'Content-Type': 'application/json'
    # }
    # dataSubmitSimulation = {
    # 'projectId': int(ProjectGen['ProjectID']),
    # 'resourceId': int(userPortalDetails['ResourceID']),
    # 'clientId': int(authData['securityGroupID']),
    # 'createdBy': authData['username'],
    # 'entitlementID': userPortalDetails['clientEntitlementID'],
    # 'portalTenantID': userPortalDetails['portalTenantID'],
    # 'portalUserID': authData['portalUserID'],
    # 'projectSimulationId': int(createSimulation['projectSimulationID']),
    # }

    # responseSubmitSimulation = requests.post(req_urlSubmitSimulation, headers=headersSubmitSimulation, data=json.dumps(dataSubmitSimulation))
    # jsonResponseSubmitSimulation = responseSubmitSimulation.json()
    # if responseSubmitSimulation.status_code == 200:
    #     submitted = str(jsonResponseSubmitSimulation)
    #     if submitted == "True":
    #         print(str(datetime.datetime.now()) + " : Simulation submitted successfully ")
    # else:
    #     print(str(datetime.datetime.now()) + " : Simulation submitted failed with an error " + str(responseSubmitSimulation.status_code))
    #     raise Exception("Simulation submitted failed with an error " + str(responseSubmitSimulation.status_code))