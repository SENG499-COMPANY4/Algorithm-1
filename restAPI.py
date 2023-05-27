#restAPI.py

from flask import Flask, request

app = Flask(__name__)

exampleSchedule = {
    "Program":"SENG", "CourseNum":499
}

@app.route("/")
def hello_world():
    return "Hello, World!"
    
@app.route("/generateSchedule", methods=['GET', 'POST'])
def generateSchedule():
    if request.method == 'GET':
        return getSchedule()
        
def getSchedule():
    return exampleSchedule
    