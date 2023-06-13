
import json
#TYPES

#class: TimeSlot
#starttimes: array corresponding to every lecture start in a week
#endtimes: respective array to starttimes but for end times
#islocked: bool value where True = locked
class TimeSlot:
  def __init__(self, starttimes[], endtimes[], islocked)
    self.starttimes[] = starttimes[]
    self.endtimes[] = endtimes[]
    self.islocked = islocked

#class: Course
#name: the name of the course
class Course:
  def __init__(self, name)
    self.name = name

#class: Prof
#name: the prof's name
class Prof:
  def __init__(self, name)
    self.name = name

#class: Room
#building: building code of room
#number: room number
class Room:
  def __init__(self, building, room)
    self.building = building
    self.room = room


#FUNCTIONS

#function: process_time_slots
#inputs: a string that holds the path of the time slot data
#outputs: an array of time slots of type TimeSlot
#description: This function processes the time slot data and returns it as a custom type
#             that can be processed by the algorithm.
#def process_time_slots(str timeSlotsFilePath)

#function: process_prof_data
#inputs: a string that holds the path of the prof data
#outputs: an array of type Prof
#description: This function processes the prof data and returns it as a custom type
#             that can be processed by the algorithm.
#def process_prof_data(str profDataPath)

#function: process_course_data
#inputs: a string that holds the path of the course data
#outputs: an array of type Course
#description: This function processes the course data and returns it as a custom type
#             that can be processed by the algorithm.
#def process_course_data(str courseDataPath)

#function: export_schedule
#inputs: the array of time slots with their assigned data, a flag to indicate an
#        impossible request
#outputs: none
#description: This function takes the time slot data and exports the schedule as a JSON.
#             If isPossible is set to 'True', don't update the exported schedule and
#             display an appropriate message.
def export_schedule(timeslots, isPossible):
    if isPossible is False:
        print("Schedule is not possible with given constraints, please adjust make adjustments")
    f = open("outData.txt", "w")
    f.write(json.dumps(timeslots, indent=4))

#function: check_possibility
#inputs: arrays of profs, courses, and rooms with all relevant data, an array of disallowed
#        placements, an array of locked placements
#outputs: a boolean value indicating if it is possible to generate a schedule
#description: This function checks if it is possible for a schedule to be determined,
#             given all provided data and any banned or locked placements.
#def check_possibility(Prof[] profs, Course[] courses, Room[] rooms, TimeSlot[] bannedPlacements, TimeSlot[] lockedPlacements)

#function: set_prof_priority
#inputs: an array of the profs with their associated data
#outputs: none
#description: This function uses a weighting algorithm to assign priority scores for profs.
#def set_prof_priority(Prof[] profs)

#function: set_course_priority
#inputs: an array of the courses with their associated data
#outputs: none
#description: This function uses a weighting algorithm to assign priority scores for courses.
#             These scores will be used when assigning rooms.
#def set_course_priority(Course[] courses)

#function: associate_priority_rooms
#inputs: the array of available rooms, the array of courses
#outputs: none
#description: This function assigns indicators of priority rooms for courses, such as
#             placing CS courses in ECS classrooms.
#def associate_priority_rooms(Room[] rooms, Course[] courses)

#function: assign_profs
#inputs: the array of profs, the array of courses
#outputs: none
#description: This function assigns profs to courses, ensuring requirements are met and
#             that preferences are met in order of their predetermined weighted priority.
def assign_profs(profs, courses):
    
    profs = get_pref_prof(profs, courses)
    profs['courses'].append(courses['coursename'])
    return profs['name']

def get_pref_prof(profs, courses):
    return profs[0]
#function: assign_rooms
#inputs: the array of rooms, the array of courses
#outputs: none
#description: This function assigns rooms to courses, ensuring requirements are met.
def assign_rooms(rooms, courses):
    
    rooms = get_pref_room(rooms, courses)
    if rooms is not None:
        return rooms['location']
    else: 
        return None
    
def get_pref_room(rooms, courses):
    
    for room in rooms:
        if room['capacity'] >= courses['capacity']:
            return room
        else:
            print("No valid room")
            return None

#function: lock_course
#inputs: the array of timeslots, the array of locked course timeslots, the course to lock
#outputs: none
#description: This function manually locks a course in a timeslot.
#def lock_course(TimeSlot[] timeslots, TimeSlot[] lockedPlacements, Course courseToLock)

#function: unlock_course
#inputs: the array of locked course timeslots, the course to lock
#outputs: none
#description: This function manually unlocks a course in a timeslot.
#def unlock_course(TimeSlot[] lockedPlacements, Course courseToUnlock)

#function: assign_slots
#inputs: the array of timeslots, the array of locked placements, the array of courses with
#        all their relevant data
#outputs: none
#description: This function uses an algorithm to assign courses to timeslots based on a
#             weighted priority.
#def assign_slots(TimeSlot[] timeslots, TimeSlot[] lockedPlacements, Course[] courses)

def get_in_data():
    f = open("inData.json", "r")
    inDataJson = f.read()
    inData = json.loads(inDataJson)
    return inData
    
    
    
def create_out_data_dict():
    outData = {
        "timeslot": 0,
        "day": [],
        "coursename": "",
        "room": "",
        "professor": "",
        "type": ""
    }
    
    return outData

def schedule_creation(inData):
    
    outDataList = []
    for courses in inData['courses']:
        print("Scheduling: " + courses['coursename'])
        outData = create_out_data_dict()
        
        outData['coursename'] = courses['coursename']
        
        outData['professor'] = assign_profs(inData['professors'], courses)
        
        outData['room'] = assign_rooms(inData['rooms'], courses)
        
        #Base requirement all secheduled courses are lectures
        outData['type'] = "lecture"
        
        outDataList.append(outData)
        #print(json.dumps(outData, indent=4))
    print("\nGenerated Schedule:\n" + json.dumps(outDataList, indent=4))
    return outDataList
        
def main():
    inData = get_in_data()
    outData = schedule_creation(inData)
    export_schedule(outData, True)

if __name__ == "__main__":
    main()