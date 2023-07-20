import datetime
import json
import random
#TYPES

#class: TimeSlot
#starttimes: array corresponding to every lecture start in a week
#endtimes: respective array to starttimes but for end times
#islocked: bool value where True = locked
#courses: list of courses assigned to the slot
class TimeSlot:
  def __init__(self, day, startTimes, length):
    self.day = day
    self.startTimes = startTimes
    self.length = length
    self.courses = []
    self.profs = []
    self.rooms = []

#class: Course
#coursename: the name of the course
#lecturesNumber: 
#labsNumber: 
#tutorialsNumber: 
#capacity: 
class Course:
  def __init__(self, coursename, noScheduleOverlap, lecturesNumber, labsNumber, tutorialsNumber, capacity):
    self.coursename = coursename
    self.noScheduleOverlap = noScheduleOverlap
    self.lecturesNumber = lecturesNumber
    self.labsNumber = labsNumber
    self.tutorialsNumber = tutorialsNumber
    self.capacity = capacity
    self.room = None

#class: Prof
#name: the prof's name
#courses: 
#timePreferences: 
#dayPreferences: 
#equipmentPreferences: 
class Prof:
  def __init__(self, name, courses, timePreferences, coursePreferences, dayPreferences, equipmentPreferences):
    self.name = name
    self.courses = courses
    self.assignedCourses = []
    self.timePreferences = timePreferences
    self.coursePreferences = coursePreferences
    self.dayPreferences = dayPreferences
    self.equipmentPreferences = equipmentPreferences

#class: Room
#building: building code of room
#number: room number
#capacity: max seats
#hastech: bool for if room is equipped for connecting technology
class Room:
  def __init__(self, location, capacity, hasTech):
    self.location = location
    self.capacity = capacity
    self.hasTech = hasTech

  def __str__(self):
    return self.building + self.number
    
globalTimeSlots = {'Lecture': [], 'Lab': [], 'Tutorial': []}



#FUNCTIONS

#function: process_time_slots
#inputs: a string that holds the path of the time slot data
#outputs: an array of time slots of type TimeSlot
#description: This function processes the time slot data and returns it as a custom type
#             that can be processed by the algorithm.
def process_time_slots(ScheduleType):

    inFile = ScheduleType + "Timeslots.json"

    f = open(inFile, "r")

    timeslotData = json.loads(f.read())
    
    time_slots = []
    
    for slotData in timeslotData['timeslots']:
        time_slots.append(TimeSlot(slotData['day'], slotData['startTime'], slotData['length']))

    return time_slots

#function: process_prof_data
#inputs: a string that holds the path of the prof data
#outputs: an array of type Prof
#description: This function processes the prof data and returns it as a custom type
#             that can be processed by the algorithm.
def process_prof_data(inData):
    profs = []

    for profData in inData['professors']:
        profs.append(Prof(profData['name'], profData['courses'], profData['timePreferences'], profData['coursePreferences'], profData['dayPreferences'], profData['equipmentPreferences']))

    return profs

#function: process_course_data
#inputs: a string that holds the path of the course data
#outputs: an array of type Course
#description: This function processes the course data and returns it as a custom type
#             that can be processed by the algorithm.
def process_course_data(inData):
    courses = []

    for courseData in inData['courses']:
        courses.append(Course(courseData['coursename'], courseData['noScheduleOverlap'], courseData['lecturesNumber'], courseData['labsNumber'], courseData['tutorialsNumber'], courseData['capacity']))

    return courses

def process_room_data(inData):
    rooms = []

    for roomData in inData['rooms']:
        rooms.append(Room(roomData['location'], roomData['capacity'], roomData['equipment']))

    return rooms


#function: export_schedule
#inputs: the array of time slots with their assigned data, a flag to indicate an
#        impossible request
#outputs: none
#description: This function takes the time slot data and exports the schedule as a JSON.
#             If isPossible is set to 'True', don't update the exported schedule and
#             display an appropriate message.
def export_schedule(timeslots):
    if check_possibility(timeslots) is False:
        print("Schedule is not possible with given constraints, please adjust make adjustments")
    f = open("currentSchedule.json", "w")
    f.write(json.dumps(timeslots, indent=4))

#function: check_possibility
#inputs: arrays of profs, courses, and rooms with all relevant data, an array of disallowed
#        placements, an array of locked placements
#outputs: a boolean value indicating if it is possible to generate a schedule
#description: This function checks if it is possible for a schedule to be determined,
#             given all provided data and any banned or locked placements.
def check_possibility(finalSchedule):
    slots = getAllTimeSlots(finalSchedule)
    for slot in slots:
        slotCourses = []
        for course in finalSchedule:
            if course['starttime'] == slot:
                slotCourses.append(course)
        print("Time: " + str(slot) + "\nCourse: " + str(slotCourses)) 
        
        profs = [i['professor'] for i in slotCourses]
        #remove none values
        profs = list(filter(lambda item: item != '', profs))
        if len(profs) != len(set(profs)):
            print("Schedule is invalid, prof conflict")
            return False        
        
        rooms = [i['room'] for i in slotCourses]
        #remove none values
        rooms = list(filter(lambda item: item is not None, rooms))
        if len(rooms) != len(set(rooms)):
            print("Schedule is invalid, room conflict")
            #return False
    return True


def getAllTimeSlots(finalSchedule):
    slots = [start['starttime'] for start in finalSchedule]
    slotList = []
    for slot in slots:
        if slot not in slotList:
            slotList.append(slot)
    return slotList

#function: set_prof_priority
#inputs: an array of the profs with their associated data
#outputs: none
#description: This function uses a weighting algorithm to assign priority scores for profs.
def set_prof_priority(profs, courses, index):
    # Do priority classes first (Start 4b and work down to 1a)
    # Get prof teaching requirements

    validProf = []
    random.shuffle(profs)

    for prof in profs:
        boolProfPriority, lenProfPriority = prof_priority(prof, courses, index)
        if boolProfPriority:
            validProf.append(prof)
        
    
    # Limit prof list to only valid profs
    # Tentatively place profs to course
    # If no prof exists the ignore preferences list
    if len(validProf) > 0:
        return validProf[0]
    elif lenProfPriority > 1:
        index += 1
        return set_prof_priority(profs, courses, index)
    else:
        return None

def prof_priority(prof, courses, index):
    requirements = [(courses.coursename in prof.courses), (len(prof.assignedCourses) <= 4)]
    reqSize = (len(requirements) - index)
    return all(requirements[:reqSize]), len(requirements[:reqSize])

#function: set_course_priority
#inputs: an array of the courses with their associated data
#outputs: none
#description: This function uses a weighting algorithm to assign priority scores for courses.
#             These scores will be used when assigning rooms.
#def set_course_priority(Course[] courses)

#function: associate_priority_rooms
#inputs: the array of available rooms, the array of courses
#outputs: list of tuples of courses matched with a list of possible rooms sorted by size
#description: This function assigns indicators of priority rooms for courses, such as
#             placing CS courses in ECS classrooms.
def associate_priority_rooms(rooms, courses):
    rooms.sort(key=lambda x: x.capacity, reverse = True)
    courses.sort(key=lambda x: x.capacity, reverse = True)
    roomPossibilities = []
    for course in courses:
        possibilities = []
        for room in rooms:
            if(course.capacity <= room.capacity and not (course.needsTech and not room.hasTech)):
                possibilities.append(room)
        roomPossibilities.append((course, possibilities))
    return roomPossibilities

#function: assign_rooms
#inputs: the array of courses, the respective array of tuples with first element being the
#        course and second element being the list of possible rooms
#outputs: none
#description: This function assigns the courses to their possible rooms based on a priority
#             by seats needed. If it can't match a course to a room the room attribute will
#             remain None.
def assign_rooms(courses, roomPossibilities):
  assignedRooms = []
  for k in range(len(courses)):
    for room in roomPossibilities[k][1]:
      if room not in assignedRooms:
        courses[k].room = room
        assignedRooms.append(room)
        break

#function: assign_profs
#inputs: the array of profs, the array of courses
#outputs: none
#description: This function assigns profs to courses, ensuring requirements are met and
#             that preferences are met in order of their predetermined weighted priority.
def assign_profs(profs, courses):
    
    prof = set_prof_priority(profs, courses, index=0)

    if prof is None:
        return None

    prof.assignedCourses.append(courses.coursename)
    return prof.name

def get_pref_prof(profs, courses):
    return profs[0]

#function: assign_rooms
#inputs: the array of rooms, the array of courses
#outputs: none
#description: This function assigns rooms to courses, ensuring requirements are met.

def assign_rooms(courses, rooms):
    
    room = get_pref_room(rooms, courses)
    if room is not None:
        return room.location
    else: 
        return None
    
def get_pref_room(rooms, courses):
    
    for room in rooms:
        if room.capacity >= courses.capacity:
            return room
        else:
            print("No valid room")
            return None

#function: lock_course
#inputs: all input data
#outputs: the array of locked courses
#description: This function manually locks a course in a timeslot.
def lock_courses(inData):
    lockedPlacements = []
    for schedule in inData['lockedSchedule']:
        lockedPlacements.append(schedule)
    return lockedPlacements

#function: remove_locked_items
#inputs: all input data
#outputs: the same input data without courses that have already been scheduled
#description: This fuction removes redundant data. In the future, it should be adapted to 
#             account for any data that the system keeps that is recorded during other
#             functions, like how many classes a professor is currently listed to teach.
def remove_locked_items(inData):
    for schedule in inData['lockedSchedule']:
        for course in inData['courses']:
            if course['coursename'] == schedule['coursename']:
                inData['courses'].remove(course)
    return inData

#function: assign_slots
#inputs: the array of timeslots, the array of locked placements, the array of courses with
#        all their relevant data
#outputs: none
#description: This function uses an algorithm to assign courses to timeslots based on a
#             weighted priority.
def create_timeslots(timeslots, Type):
    print(Type)
    for slots in timeslots:
        Week = {'Monday': None, 'Tuesday': None, 'Wednesday': None, 'Thursday': None, 'Friday': None}
        for day in slots.day:
            Week[day] = slots.startTimes
        globalTimeSlots[Type].append(TimeSlot(Week, Week, 0))
    
    for i in range(len(globalTimeSlots[Type])):
        print(globalTimeSlots[Type][i].startTimes)

def assign_slots(course, prof, Type):
  #for now just assigning at random and ignoring locked courses
  #this assumes by the time this function is called the courses will have all required data in their data type
  #for course in courses:
    #slot = random.randint(0,len(globalTimeSlots)-1)
    outDay = {}
    for slot in globalTimeSlots[Type]:
        if len([i for i in course.noScheduleOverlap if i in slot.courses]) == 0\
        and course.coursename not in slot.courses\
        and ((prof is None) or (prof not in slot.profs)):
            print()
            slot.courses.append(course.coursename)
            slot.profs.append(prof)

            print("Timeslot: " + str(slot.courses))
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                if slot.startTimes[day] is not None:
                    outDay[day] = slot.startTimes[day]
            print(outDay)
            break
        print()
        
    return outDay

def checkTimeslotOverlap():
    pass

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

    #Parse out data that doesn't need to be scheduled, locked schedule components
    if 'lockedSchedule' in inData:
        outDataList = lock_courses(inData)
        inData = remove_locked_items(inData)

    courses = process_course_data(inData)
    profs = process_prof_data(inData)
    rooms = process_room_data(inData)

    #print(json.dumps(inData, indent=4))
    for course in courses:
        print("Scheduling: " + course.coursename)
        outData = create_out_data_dict()
        
        outData['coursename'] = course.coursename
        
        outData['professor'] = assign_profs(profs, course)
        
        outData['starttime'] = assign_slots(course, outData['professor'], "Lecture")
        
        outData['room'] = assign_rooms(course, rooms)
        
        #Base requirement all secheduled courses are lectures
        outData['type'] = "Lecture"
        
        outDataList.append(outData)

    for course in courses:
        for i in range(course.labsNumber):
            print("Scheduling Labs: " + course.coursename)
            outData = create_out_data_dict()
        
            outData['coursename'] = course.coursename

            outData['starttime'] = assign_slots(course, None, "Lab")
        
            outData['room'] = assign_rooms(course, rooms)

            outData['type'] = "Lab"
        
            outDataList.append(outData)
    
    for course in courses:
        for i in range(course.tutorialsNumber):
            print("Scheduling Labs: " + course.coursename)
            outData = create_out_data_dict()
        
            outData['coursename'] = course.coursename

            outData['starttime'] = assign_slots(course, None, "Tutorial")
        
            outData['room'] = assign_rooms(course, rooms)

            outData['type'] = "Tutorial"
        
            outDataList.append(outData)

    print("\nGenerated Schedule:\n" + json.dumps(outDataList, indent=4))
    return outDataList
        
def main():
    inData = get_in_data()

    lectureTimeSlots = process_time_slots("Lecture")
    labTimeSlots = process_time_slots("Lab")
    TutorialTimeSlots = process_time_slots("Tutorial")

    create_timeslots(lectureTimeSlots, "Lecture")
    create_timeslots(labTimeSlots, "Lab")
    create_timeslots(TutorialTimeSlots, "Tutorial")

    outData = schedule_creation(inData)
    export_schedule(outData)

if __name__ == "__main__":
    main()
