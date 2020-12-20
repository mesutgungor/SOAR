#This script will help you to unisolate machines that have been isolated FP ly and automatically in bulk, using Python requests library
#You should get the api token from this web page https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-atp/apis-intro

import json
import requests
from datetime import datetime
import time

headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer you_get_this_token_from_Azure'
        
}

#You have to add comment to the payload
payload ="{'Comment' : 'unisolate_via_api'}"
api_url="https://api-us.securitycenter.windows.com/api/machineactions/"

#To find out which machines have been isolated we get the all the machineactions
response = requests.get(api_url,headers=headers)

devices = response.json()
for device in devices["value"]:
    if(device["type"]=="Isolate"):
    	response2 = requests.post("https://api-eu.securitycenter.windows.com/api/machines/"+device["machineId"]+"/unisolate",data=payload,headers=headers)
    	print(response2.status)
    	print(device["machineId"])
    	time.sleep(2)
