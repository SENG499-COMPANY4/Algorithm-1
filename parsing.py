import json

def readData(filename): #read in the requirements data
        df = open(filename, "r")
        requirements = json.load(df)
        df.close()
        return requirements

req = readData("recentData.json")
rooms = req["rooms"]
timeslots = req["timeslots"]
courses = req["courses"]
professors = req["professors"]

print(rooms[0])