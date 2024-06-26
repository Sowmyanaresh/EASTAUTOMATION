import requests
import json
import datetime

import psycopg2
import pandas.io.sql as psql
#import config
import json

import pyodbc

# def downloadRawCSVAzureSP(authData,ProjectSimID):                    
#     server = authData['azureServer']
#     database = authData['azureDatabase']
#     username = authData['azureUsername']
#     password = authData['azurePassword']
dbUser = 'SolarisAdmin@psql-dev-cyt-solara-eastus' #authData['dbUsername']
dbPassword = 's8l7_i#=P)3#' #authData['dbPassword']

                            
# prerequisite - get the ip address approved
ProjectSimID = 29974
ProjectName = 'MultiArmHochberg'
test_env = 'test6'


# host = "psql-11-dev-cyt-solaris-eastus.postgres.database.azure.com"
host = 'psql-dev-cyt-solara-eastus.postgres.database.azure.com'
dbname = f'solara_{test_env}'

connection = psycopg2.connect(host = host, dbname= dbname, user=dbUser, password=dbPassword, sslmode='prefer')#, sslrootcert='BaltimoreCyberTrustRoot.crt.pem')
dataframe = psql.read_sql(f'SELECT * FROM result."SimModelResultDataLakeSettings"  WHERE "ProjectSimulationID" = {ProjectSimID} ORDER BY "ID" DESC', connection)

print(dataframe)
print(dataframe.columns)