import requests
import pytest
import json
import requests_mock

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

def getRequest(address, route, auth=True):
    
    if auth is True:
        authToken = BearerAuth(getAccessToken())
    else:
        authToken = ''
    
    r = requests.get(str(address + route), auth= authToken)
    return r

def postRequest(address, route, body, auth=True):

    if auth is True:
        authToken = BearerAuth(getAccessToken())
    else:
        authToken = ''
    
    r = requests.post(str(address + route), auth = authToken, json = body)
    return r

def putRequest(address, route, body):
    
    r = requests.put(str(address + route), auth = BearerAuth(getAccessToken()), json = body)
    return r


#***TESTCASES***

def test_APIGetScheduleValid():

    environment = getAddress('Stage')
    response = getRequest(environment, '/generateSchedule')
    
    assert int(response.status_code) == 200

def test_APIGetScheduleNoAuth():
    environment = getAddress('Stage')
    response = getRequest(environment, '/generateSchedule', False)
    
    assert int(response.status_code) == 401

def test_APIPostValid():


    environment = getAddress('Stage')
    response = postRequest(environment, '/generateSchedule', 
        {
            "courses": [{
                "noScheduleOverlap": ["ENGR 110", "ENGR 130", "MATH 100", "MATH 109", "MATH 110", "PHYS 110"],
                "coursename": "CSC 111",
                "capacity": 100,
                "labsNumber": 8,
                "tutorialsNumber": 0,
                "lecturesNumber": 1
            }],
            "professors": [{
                "coursePreferences": [],
                "courses": ["CSC 445", "CSC 545", "CSC 111", "CSC 116", "CSC 497"],
                "dayPreferences": [],
                "equipmentPreferences": [],
                "name": "Bird, Bill",
                "timePreferences": []
            }],
            "rooms": [{
                "capacity": 100,
                "equipment": ["2 x Pulldown Screens", "Chalk Board 6ft", "Chalk Board, Sliding, 2 x 6ft + 12ft behind slides", "Desktop Lecture Capture with Webcam", "Digital Classroom (HDMI and VGA connections)", "Document Camera", "PC Computer", "Screen - centre", "Video Data Projector", "iClicker Receiver"],
                "location": "ECS 104"
            }]
        }
    )

    assert int(response.status_code) == 200
    '''
    # Mock the successful API response for the valid case
    mock_request_data = {"data": "sample data for POST request"}
    mock_response_data = {"status": "success"}
    mock_status_code = 200

    # Start the mocking session
    with requests_mock.Mocker() as m:
        # Mock the response for the API endpoint
        environment = 'Stage'
        base_address = getAddress(environment)
        mock_route = '/submitData'
        m.post(base_address + mock_route, json=mock_response_data, status_code=mock_status_code)

        # Now, call the postRequest function without tokens
        response = postRequest(base_address, mock_route, mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data
    '''

def test_APIPostInvalid():
    environment = getAddress('Stage')
    response = postRequest(environment, '/generateSchedule', 
        {
            "courses": [{
                "noScheduleOverlap": ["ENGR 110", "ENGR 130", "MATH 100", "MATH 109", "MATH 110", "PHYS 110"],
                "coursename": "CSC 111",
                "capacity": 100,
                "labsNumber": 8,
                "tutorialsNumber": 0,
                "lecturesNumber": 1
            }],
            "professors": [{
                "coursePreferences": [],
                "courses": ["CSC 445", "CSC 545", "CSC 111", "CSC 116", "CSC 497"],
                "dayPreferences": [],
                "equipmentPreferences": [],
                "name": "Bird, Bill",
                "timePreferences": []
            }]
        }
    )

    assert int(response.status_code) == 500
    '''
    # Mock the API response for the invalid case
    mock_request_data = {"data": "invalid data for POST request"}
    mock_response_data = {"error": "Invalid data"}
    mock_status_code = 500

    # Start the mocking session
    with requests_mock.Mocker() as m:
        # Mock the response for the API endpoint
        environment = 'Stage'
        base_address = getAddress(environment)
        mock_route = '/submitData'
        m.post(base_address + mock_route, json=mock_response_data, status_code=mock_status_code)

        # Now, call the postRequest function without tokens
        response = postRequest(base_address, mock_route, mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data
    '''

def test_APIPostNoToken():
    environment = getAddress('Stage')
    response = postRequest(environment, '/generateSchedule', 
        {
            "courses": [{
                "noScheduleOverlap": ["ENGR 110", "ENGR 130", "MATH 100", "MATH 109", "MATH 110", "PHYS 110"],
                "coursename": "CSC 111",
                "capacity": 100,
                "labsNumber": 8,
                "tutorialsNumber": 0,
                "lecturesNumber": 1
            }],
            "professors": [{
                "coursePreferences": [],
                "courses": ["CSC 445", "CSC 545", "CSC 111", "CSC 116", "CSC 497"],
                "dayPreferences": [],
                "equipmentPreferences": [],
                "name": "Bird, Bill",
                "timePreferences": []
            }],
            "rooms": [{
                "capacity": 100,
                "equipment": ["2 x Pulldown Screens", "Chalk Board 6ft", "Chalk Board, Sliding, 2 x 6ft + 12ft behind slides", "Desktop Lecture Capture with Webcam", "Digital Classroom (HDMI and VGA connections)", "Document Camera", "PC Computer", "Screen - centre", "Video Data Projector", "iClicker Receiver"],
                "location": "ECS 104"
            }]
        }
    , False)

    assert int(response.status_code) == 401
    '''
    # Mock the API response when making a POST request without a token
    mock_request_data = {"data": "sample data for POST request"}
    mock_response_data = {"error": "Unauthorized"}
    mock_status_code = 401

    # Start the mocking session
    with requests_mock.Mocker() as m:
        # Mock the response for the API endpoint
        environment = 'Stage'
        base_address = getAddress(environment)
        mock_route = '/submitData'
        m.post(base_address + mock_route, json=mock_response_data, status_code=mock_status_code)

        # Now, call the postRequest function without tokens
        response = postRequest(base_address, mock_route, mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data
    '''

def test_APIPutScheduleInvalid():

    environment = getAddress('Stage')
    response = putRequest(environment, '/generateSchedule', {"test": "test"})

    assert int(response.status_code) == 500

def test_APIPutScheduleNoAuth():

    response = requests.put('https://schedulingalgorithmstaging.azurewebsites.net/generateSchedule', json = 
        {
            "coursename": "SENG499",
            "year": 4,
            "timeslot": "Wednesday @ 3:00",
            "schedule": ["item", "item2"]
        }
    )

    assert int(response.status_code) == 401

def test_APIPutScheduleValid():

    environment = getAddress('Stage')
    response = putRequest(environment, '/generateSchedule', 
        {
            "coursename": "SENG499",
            "year": 4,
            "timeslot": "Wednesday @ 3:00",
            "schedule": ["item", "item2"]
        }
    )

    assert int(response.status_code) == 200

def test_APIPutDataSaved():

    environment = getAddress('Stage')
    response = putRequest(environment, '/generateSchedule', 
        {
            "coursename": "SENG499",
            "year": 4,
            "timeslot": "Wednesday @ 3:00",
            "schedule": ["item", "item2"]
        }
    )

    assert response.json() == ["item", "item2"]

def test_APIValidate():

    environment = getAddress('Stage')
    response = postRequest(environment, '/validate', [
    {
        "starttime": {
            "Monday": 830,
            "Thursday": 830
        },
        "coursename": "SENG499",
        "room": "ECS123",
        "professor": "Navneet Popli",
        "type": "Lecture"
    },
    {
        "starttime": {
            "Monday": 1000,
            "Thursday": 1000
        },
        "coursename": "SENG440",
        "room": "CLE288",
        "professor": "Prof A",
        "type": "Lecture"
    },
    {
        "starttime": {
            "Monday": 1130
        },
        "coursename": "SENG474",
        "room": "ECS123",
        "professor": "Prof B",
        "type": "Lab"
    }]
    )

    assert int(response.status_code) == 200

def test_APIValidateNoAuth():

    response = requests.post('https://schedulingalgorithmstaging.azurewebsites.net/validate', json = [
        {
            "starttime": {
                "Monday": 830,
                "Thursday": 830
            },
            "coursename": "SENG499",
            "room": "ECS123",
            "professor": "Navneet Popli",
            "type": "Lecture"
        },
        {
            "starttime": {
                "Monday": 1000,
                "Thursday": 1000
            },
            "coursename": "SENG440",
            "room": "CLE288",
            "professor": "Prof A",
            "type": "Lecture"
        },
        {
            "starttime": {
                "Monday": 1130
            },
            "coursename": "SENG474",
            "room": "ECS123",
            "professor": "Prof B",
            "type": "Lab"
        }]
    )

    assert int(response.status_code) == 401


#Run tests!
if __name__ == "__main__":
    test_APIGetScheduleValid()
    test_APIGetScheduleNoAuth()
    test_APIPostValid()
    test_APIPostInvalid()
    test_APIPostNoToken()
    test_APIPutScheduleInvalid()
    test_APIPutScheduleNoAuth()
    test_APIPutScheduleValid()
    test_APIPutDataSaved()
    test_APIValidate()
    test_APIValidateNoAuth()
    print("All passed!")
