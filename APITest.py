import requests
import pytest
import json

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        
        self.token = token
        
    def __call__(self, r):
    
        r.headers['authorization'] = "Bearer " + str(self.token)
        return r

#***HELPER FUNCTIONS***

def getAddress(environment):
    if environment == 'Stage':
        return 'https://schedulingalgorithmstaging.azurewebsites.net'
    elif environment == 'Prod':
        return 'https://schedulingalgorithmapi.azurewebsites.net'
    else:
        print("Invalid Environment: Please use \'Stage\' or \'Prod\'")

def getAccessToken():
    
    f = open('requestData.json')
    
    requestPayload = json.load(f)
    
    r = requests.post('https://login.microsoftonline.com/organizations/oauth2/v2.0/token', data= requestPayload)
    bearerToken = r.json()["access_token"]
    return bearerToken

def getRequest(address, route):
    
    r = requests.get(str(address + route), auth= BearerAuth(getAccessToken()))
    return r

def postRequest():
    pass

def putRequest():
    pass


#***TESTCASES***

def test_APIGetScheduleValid():

    environment = getAddress('Stage')
    response = getRequest(environment, '/generateSchedule')
    
    assert int(response.status_code) == 200
