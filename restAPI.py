#restAPI.py

from flask import Flask, request
import SchedulingAlgorithm
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"
    
#Endpoint for main data transfer between backend and Algo 1
#GET: receives most recently generated schedule
#POST: sends new data to genrate a new schedule
#PUT: makes alterations to current data to generate a new schedule
@app.route("/generateSchedule", methods=['GET', 'POST', 'PUT'])
def generateSchedule():
    if request.method == 'GET':
        return getSchedule()
    elif request.method == 'POST':
        return saveData()
    elif request.method == 'PUT':
         return editData()
         
#Endpoint for Company 3 integration
@app.route("/schedule/create", methods=['GET', 'POST', 'PUT'])
def comp3Create():
    if request.method == 'GET':
        return getSchedule()
    elif request.method == 'POST':
        return saveData()
    elif request.method == 'PUT':
         return editData()

#Endpoint to validate a schedule
#Ensures schedule generated matches real-world requirements
@app.route("/validate", methods=['POST'])
def validateSchedule():
    if request.method == 'POST':
        return validateData()

#Endpoint to validate a schedule for Company 3
@app.route("/schedule/validate", methods=['POST'])
def comp3ValidateSchedule():
    if request.method == 'POST':
        return validateData()
    
#Return the currently generated schedule
def getSchedule():
    return readData()

#Save newly imported data from backend to the json object
def saveData():
	df = open("recentData.json", "r+") #df = data file
	df.truncate(0)
	data = json.dumps(request.json)
	df.write(data)
	df.close()
	SchedulingAlgorithm.main()
	return getSchedule()

#Open and return the currently genrated schedule
def readData():
    rf = open("currentSchedule.json", "r") #rf = result file
    currentSchedule = rf.read()
    rf.close()
    return currentSchedule

#Save alterations to current data and regenerate the schedule
def editData():
    df = open("recentData.json", "r+") #data file
    rf = open("currentSchedule.json", "r+") #result file
    df.truncate(0)
    rf.truncate(0)
    data = json.dumps(request.json)
    currentSchedule = json.dumps(request.json['schedule'])
    df.write(data)
    rf.write(currentSchedule)
    df.close()
    rf.close()
    return getSchedule()

#Validate a schedule against real-world possible data
def validateData():
    
    data = []
    for i in request.json:
        data.append(i)
    
    return str(SchedulingAlgorithm.check_possibility(data))
