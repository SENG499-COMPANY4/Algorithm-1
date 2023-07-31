# Algorithm-1
Algorithm 1 for course scheduling project

## Local Run

To run on a local machine:

pip install -r requirements.txt

flask --app restAPI run

## Testing

To run testcases, install requestData.json to file directory

pytest APITest.py

NOTE: All added testcase functions must start with 'test_' or they will not be recognized by pytest

## Azure

To configure the API on Azure, you will first need to create an API app and link your github repo. Any additional configuration options should be determined by the developer. The required startup command is:

gunicorn -w 4 -b 0.0.0.0 'wsgi:app'
