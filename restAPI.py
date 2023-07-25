#restAPI.py

from flask import Flask, request
import SchedulingAlgorithm
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"
    
@app.route("/generateSchedule", methods=['GET', 'POST', 'PUT'])
def generateSchedule():
    if request.method == 'GET':
        return getSchedule()
    elif request.method == 'POST':
        return saveData()
    elif request.method == 'PUT':
         return editData()

@app.route("/validate", methods=['POST'])
def validateSchedule():
    if request.method == 'POST':
        return validateData()
    
def getSchedule():
    return readData()

def saveData():
	df = open("recentData.json", "r+") #df = data file
	df.truncate(0)
	data = json.dumps(request.json)
	df.write(data)
	df.close()
	SchedulingAlgorithm.main()
	return getSchedule()

def readData():
    rf = open("currentSchedule.json", "r") #rf = result file
    currentSchedule = rf.read()
    rf.close()
    return currentSchedule

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

def validateData():
    
    data = []
    for i in request.json:
        data.append(i)
    
    return str(SchedulingAlgorithm.check_possibility(data))
