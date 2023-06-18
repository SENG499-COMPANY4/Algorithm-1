import datetime
import json
#TYPES

#class: TimeSlot
#starttimes: array corresponding to every lecture start in a week
#endtimes: respective array to starttimes but for end times
#islocked: bool value where True = locked
#courses: list of courses assigned to the slot
class TimeSlot:
  def __init__(self, starttimes, endtimes, islocked, courses):
    self.starttimes = starttimes
    self.endtimes = endtimes
    self.islocked = islocked
    self.courses = courses

#class: Course
#coursename: the name of the course
#lecturesNumber: 
#labsNumber: 
#tutorialsNumber: 
#capacity: 
class Course:
  def __init__(self, name, lecturesNumber, labsNumber, tutorialsNumber, capacity):
    self.coursename = coursename
    self.lecturesNumber = lecturesNumber
    self.labsNumber = labsNumber
    self.tutorialsNumber = tutorialsNumber
    self.capacity = capacity

#class: Prof
#name: the prof's name
#courses: 
#timePreferences: 
#dayPreferences: 
#equipmentPreferences: 
class Prof:
  def __init__(self, name, courses, timePreferences, dayPreferences, equipmentPreferences):
    self.name = name
    self.courses = courses
    self.timePreferences = timePreferences
    self.dayPreferences = dayPreferences
    self.equipmentPreferences = equipmentPreferences

#class: Room
#building: building code of room
#number: room number
class Room:
  def __init__(self, building, room):
    self.building = building
    self.room = room
    
globalTimeSlots = []


#FUNCTIONS

#function: process_time_slots
#inputs: a string that holds the path of the time slot data
#outputs: an array of time slots of type TimeSlot
#description: This function processes the time slot data and returns it as a custom type
#             that can be processed by the algorithm.
def process_time_slots(timeSlotsFilePath):
    time_slots = []
    
    with open(timeSlotsFilePath, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            slot_data = line.strip().split(',')
            
            if len(slot_data) == 2:
                start_time = slot_data[0].strip()
                end_time = slot_data[1].strip()
                
                # Create a new TimeSlot object and add it to the list
                time_slot = TimeSlot(start_time, end_time)
                time_slots.append(time_slot)
    
    return time_slots

#function: process_prof_data
#inputs: a string that holds the path of the prof data
#outputs: an array of type Prof
#description: This function processes the prof data and returns it as a custom type
#             that can be processed by the algorithm.
def process_prof_data(profDataPath):
    profs = []

    with open(profDataPath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            prof_data = line.strip().split(',')

            if len(prof_data) == 3:
                name = prof_data[0].strip()
                department = prof_data[1].strip()
                office = prof_data[2].strip()

                # Create a new Prof object and add it to the list
                prof = Prof(name, department, office)
                profs.append(prof)

    return profs

#function: process_course_data
#inputs: a string that holds the path of the course data
#outputs: an array of type Course
#description: This function processes the course data and returns it as a custom type
#             that can be processed by the algorithm.
def process_course_data(courseDataPath):
    courses = []

    with open(courseDataPath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            course_data = line.strip().split(',')

            if len(course_data) == 3:
                course_code = course_data[0].strip()
                course_name = course_data[1].strip()
                department = course_data[2].strip()

                # Create a new Course object and add it to the list
                course = Course(course_code, course_name, department)
                courses.append(course)

    return courses

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
    f = open("currentSchedule.json", "w")
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
#inputs: the array of locked course timeslots, the course to lock
#outputs: none
#description: This function manually locks a course in a timeslot.
def lock_course(lockedPlacements, courseToLock):
    #assuming if lockedPlacements is null it was initialized already as an empty array
    lockedPlacements.append(courseToLock)
    return None

#function: unlock_course
#inputs: the array of locked course timeslots, the course to lock
#outputs: none
#description: This function manually unlocks a course in a timeslot.
def unlock_course(lockedPlacements, courseToUnlock):
    if courseToUnlock in lockedPlacements:
        lockedPlacements.remove(courseToUnlock)
        return None

#function: assign_slots
#inputs: the array of timeslots, the array of locked placements, the array of courses with
#        all their relevant data
#outputs: none
#description: This function uses an algorithm to assign courses to timeslots based on a
#             weighted priority.
import random

def create_timeslots(timeslots):
        
    for slots in timeslots:
        Week = {'Monday': None, 'Tuesday': None, 'Wednesday': None, 'Thursday': None, 'Friday': None}
        for day in slots['day']:
            Week[day] = slots['startTime']
        globalTimeSlots.append(TimeSlot(Week, [], False, []))
    print(globalTimeSlots[1].starttimes)

def assign_slots(lockedPlacements, course):
  #for now just assigning at random and ignoring locked courses
  #this assumes by the time this function is called the courses will have all required data in their data type
  #for course in courses:
    slot = random.randint(0,len(globalTimeSlots)-1)
    globalTimeSlots[slot].courses.append(course)
    print(globalTimeSlots[slot].courses)
    
    outDay = {}
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if globalTimeSlots[slot].starttimes[day] is not None:
            outDay[day] = globalTimeSlots[slot].starttimes[day]
    
    return outDay

def get_in_data():
    f = open("recentData.json", "r")
    inDataJson = f.read()
    inData = json.loads(inDataJson)
    return inData
    
    
    
def create_out_data_dict():
    outData = {
        "starttime": "",
        #"day": [],
        "coursename": "",
        "room": "",
        "professor": "",
        "type": ""
    }
    
    return outData

def schedule_creation(inData):
    
    outDataList = []
    
    #print(json.dumps(inData, indent=4))
    for courses in inData['courses']:
        print("Scheduling: " + courses['coursename'])
        outData = create_out_data_dict()
        
        outData['coursename'] = courses['coursename']
        
        outData['professor'] = assign_profs(inData['professors'], courses)
        
        outData['starttime'] = assign_slots(False, courses['coursename'])
        
        outData['room'] = assign_rooms(inData['rooms'], courses)
        
        #Base requirement all secheduled courses are lectures
        outData['type'] = "lecture"
        
        outDataList.append(outData)
        #
    print("\nGenerated Schedule:\n" + json.dumps(outDataList, indent=4))
    return outDataList
        
def main():
    inData = get_in_data()
    create_timeslots(inData['timeslots'])
    outData = schedule_creation(inData)
    export_schedule(outData, True)

if __name__ == "__main__":
    main()
