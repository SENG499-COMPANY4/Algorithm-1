#restAPI.py

from flask import Flask, request
import SchedulingAlgorithm

app = Flask(__name__)

#exampleSchedule = {
#    "Program":"SENG", "CourseNum":499
#}

@app.route("/")
def hello_world():
    return "Hello, World!"
    
@app.route("/generateSchedule", methods=['GET', 'POST'])
def generateSchedule():
    if request.method == 'GET':
        return getSchedule()
    elif request.method == 'POST':
        return saveData()
    
def getSchedule():
    return readData()

def saveData():
        file = open("inData.txt", "r+")
        file.write(str(request.json))
        file.close()
        SchedulingAlgorithm.main()
        return getSchedule()

def readData():
        file = open("outData.txt", "r")
        exampleSchedule = file.read()
        file.close()
        return exampleSchedule