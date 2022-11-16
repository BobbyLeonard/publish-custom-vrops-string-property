import os
import requests
requests.packages.urllib3.disable_warnings()
import getpass
import re
import time
import json
import sys
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


RED  = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
BLUE='\33[44m'
BOLD = '\033[1m'
FFORMAT = '\033[0m'

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

requestTypes=['GET','POST','PUT','PATCH','DELETE']

def acquireToken():    
    #Create dict to pass as json in body
    AuthInfo = {}
    AuthInfo["username"] = username
    AuthInfo["password"] = password

    #Token Request & Parsing
    TokenEndpoint="/auth/token/acquire"
    URL=FQDN + TokenEndpoint
    r = requests.post(URL, json=AuthInfo, headers=headers, verify=False)
    output = r.text
    
    if r.status_code != 200:
        print('\n\n'+BOLD+'Response code from vROps : {}'.format(r.status_code)+FFORMAT)
        print(BOLD+'Cannot login to vROps API, exiting...\n'+FFORMAT)
        sys.exit()
        
    vROpsToken=output.split(',')[0].split(':', 1)[1][1:-1]
    #Add the Authorization Token to the header 
    headers["Authorization"] = "vRealizeOpsToken " + vROpsToken

def addProperty(objectID, timestamp, statKey, value):
    APIEndpoint = FQDN + "/resources/{}/properties".format(objectID)
    timestamplist = []
    timestamplist.append(timestamp)
    valueslist=[]
    valueslist.append(value)
    Dict = {"statKey" : statKey, "timestamps" : timestamplist, "values" : valueslist}
    jsonDict = json.dumps(Dict)
    strjsonDict = str(jsonDict)
    outstring = '''{"property-content" : [ ''' + strjsonDict + ''' ] }'''
    jsonString=json.loads(outstring)
    print('\n\n'+BOLD+'Request Body :\n'+FFORMAT)
    print(json.dumps(jsonString, indent=4, sort_keys=True))
    r = requests.post(APIEndpoint, headers=headers, verify=False, json=jsonString)
    if len(r.text) > 0:
        purposeStr = 'Response :'
        print('\n\n' + (len(purposeStr) * '~') + '\n' + BOLD + purposeStr + FFORMAT + '\n' + len(purposeStr) * '~')
        pretty_json = json.loads(r.text)
        print(json.dumps(pretty_json, indent=4, sort_keys=True))
    else :
        print('\n\n'+BOLD+'Response code from vROps : {}\n'.format(r.status_code)+FFORMAT)
    

FQDN=config["vrops"]["FQDN"]
FQDN="https://" + FQDN + "/suite-api/api"

username=config["vrops"]["username"]
password=config["vrops"]["password"]
objectID=config["vrops"]["objectID"]
statKey=config["vrops"]["statKey"]
value=config["vrops"]["value"]

acquireToken()


timestamp = time.time() * 1000
addProperty(objectID, timestamp, statKey, value)






