import pytest
import requests_mock

# Assuming getRequest function is already defined in the script.

# ***TESTCASES*** this is for test case with GET witout token 

def test_APIGetScheduleUnauthorized():
    # Mock the 401 Unauthorized API response
    mock_response_data = {"error": "Unauthorized"}
    mock_status_code = 401

    # Start the mocking session
    with requests_mock.Mocker() as m:
        # Mock the response for the API endpoint
        environment = 'Stage'
        base_address = getAddress(environment)
        mock_route = '/generateSchedule'
        m.get(base_address + mock_route, json=mock_response_data, status_code=mock_status_code)

        # Now, call the getRequest function without tokens
        response = getRequest(base_address, mock_route)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data

def test_APIPostValid():
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
        response = postRequest(base_address, mock_route, data=mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data

def test_APIPostInvalid():
    # Mock the API response for the invalid case
    mock_request_data = {"data": "invalid data for POST request"}
    mock_response_data = {"error": "Invalid data"}
    mock_status_code = 400

    # Start the mocking session
    with requests_mock.Mocker() as m:
        # Mock the response for the API endpoint
        environment = 'Stage'
        base_address = getAddress(environment)
        mock_route = '/submitData'
        m.post(base_address + mock_route, json=mock_response_data, status_code=mock_status_code)

        # Now, call the postRequest function without tokens
        response = postRequest(base_address, mock_route, data=mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data

def test_APIPostNoToken():
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
        response = postRequest(base_address, mock_route, data=mock_request_data)

    # Assertions
    assert int(response.status_code) == mock_status_code
    assert response.json() == mock_response_data
# Run the test
if __name__ == "__main__":
    pytest.main()
