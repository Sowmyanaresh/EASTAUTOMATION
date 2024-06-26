import pandas as pd
import json

def readJson(IAjson,jsonDir):
    '''
    rowNum: Takes value from 1 to n
    csvName: Name of the csv file which has the JSON names in it
    '''
    json_file = IAjson
    f = open(f'{jsonDir}\\{json_file}.json',encoding='utf-8')
    # returns JSON object as
    # a dictionary
    readJson = {
        'iajson' : json.load(f),
        'json_file' : json_file
    }
    f.close()
    return readJson