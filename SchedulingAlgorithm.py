from datetime import *
import json
import random
import math
from copy import deepcopy

#TYPES

class TimeSlot:
  def __init__(self, day, startTimes, length, sortkey=None):
    self.day = day
    self.startTimes = startTimes
    self.length = length
    self.sortkey = sortkey
    self.courses = []
    self.profs = []
    self.rooms = []


class Course:
  def __init__(self, coursename, noScheduleOverlap, lecturesNumber, labsNumber, tutorialsNumber, capacity):
    self.coursename = coursename
    self.noScheduleOverlap = noScheduleOverlap
    self.lecturesNumber = lecturesNumber
    self.labsNumber = labsNumber
    self.tutorialsNumber = tutorialsNumber
    self.capacity = capacity
    self.room = None
    self.type = None


class Prof:
  def __init__(self, name, courses, timePreferences, coursePreferences, dayPreferences, equipmentPreferences):
    self.name = name
    self.courses = courses
    self.assignedCourses = []
    self.timePreferences = timePreferences
    self.coursePreferences = coursePreferences
    self.dayPreferences = dayPreferences
    self.equipmentPreferences = equipmentPreferences


class Room:
  def __init__(self, location, capacity, hasTech):
    self.location = location
    self.capacity = capacity
    self.hasTech = hasTech

  def __str__(self):
    return self.location
    
globalTimeSlots = {'Lecture': [], 'Lab': [], 'Tutorial': []}



#FUNCTIONS

#function: process_time_slots
#description: This function processes the time slot data and returns it as a custom type
#             that can be processed by the algorithm.
def process_time_slots(ScheduleType):

    inFile = ScheduleType + "Timeslots.json"

    f = open(inFile, "r")

    timeslotData = json.loads(f.read())
    
    time_slots = []

    for slotData in timeslotData['timeslots']:
        time = datetime.strptime(slotData['startTime'], "%H:%M")
        time_slots.append(TimeSlot(slotData['day'], time, slotData['length']))

    return time_slots


#function: process_prof_data
#description: This function processes the prof data and returns it as a custom type
#             that can be processed by the algorithm.
def process_prof_data(inData):
    profs = []

    for profData in inData['professors']:
        profs.append(Prof(profData['name'], profData['courses'], profData['timePreferences'], profData['coursePreferences'], profData['dayPreferences'], profData['equipmentPreferences']))

    return profs


#function: process_course_data
#description: This function processes the course data and returns it as a custom type
#             that can be processed by the algorithm.
def process_course_data(inData):
    courses = []

    for courseData in inData['courses']:
        courses.append(Course(courseData['coursename'], courseData['noScheduleOverlap'], courseData['lecturesNumber'], courseData['labsNumber'], courseData['tutorialsNumber'], courseData['capacity']))

    return courses


#function: process_room_data
#description: This function processes the room data and returns it as a custom type
#             that can be processed by the algorithm.
def process_room_data(inData):
    rooms = []

    for roomData in inData['rooms']:
        rooms.append(Room(roomData['location'], roomData['capacity'], roomData['equipment']))

    return rooms


#function: export_schedule
#description: This function takes the time slot data and exports the schedule as a JSON.
#             If isPossible is set to 'True', don't update the exported schedule and
#             display an appropriate message.
def export_schedule(timeslots):
    if check_possibility(timeslots)['valid'] is False:
        print("Schedule is not possible with given constraints, please make adjustments")
    else:
        print("Schedule is valid")
    f = open("currentSchedule.json", "w")
    f.write(json.dumps(timeslots, indent=4, default=jsonSerial))


#function: check_possibility
#description: This function checks if it is possible for a schedule to be determined,
#             given all provided data and any banned or locked placements.
def check_possibility(finalSchedule):

    outDict = {
        'valid' : True
    }
    
    globalTimeSlots['Validate'] = []
    ValidateTimeslots = process_time_slots("Validate")
    create_timeslots(ValidateTimeslots, "Validate")

    assignmentTimeSlots = globalTimeSlots['Validate']
    allTimeSlots = globalTimeSlots['Lecture'] + globalTimeSlots['Lab'] + globalTimeSlots['Tutorial']
    for slot in assignmentTimeSlots:
        slotDay = list(filter(lambda x: slot.day[x] is not None, slot.day))[0]
        slotTime = slot.day[slotDay]
        slotLength = slot.length
        pass
        dateList = [d for d in finalSchedule if ((slotDay in d['starttime'] and d['starttime'][slotDay] is not None) and (datetime.strptime(d['starttime'][slotDay], "%H:%M") >= (slotTime) and datetime.strptime(d['starttime'][slotDay], "%H:%M") < (slotTime + timedelta(minutes=slotLength))))]

        profs = [i['professor'] for i in dateList]
        profs = list(filter(lambda item: item is not None, profs))
        #remove none values
        profs = list(filter(lambda item: item != '', profs))
        if len(profs) != len(set(profs)):
            print("Schedule is invalid, prof conflict")
            outDict['valid'] = False
            return outDict        
        
        rooms = [i['room'] for i in dateList]
        #remove none values
        rooms = list(filter(lambda item: item is not None, rooms))
        if len(rooms) != len(set(rooms)):
            print("Schedule is invalid, room conflict")
            outDict['valid'] = False
            return outDict   

    return outDict


#function: getAllTimeSlots
#description: This function returns a list of all time slots from a schedule.
def getAllTimeSlots(finalSchedule):
    slots = [start['starttime'] for start in finalSchedule]
    slotList = []
    for slot in slots:
        if slot not in slotList:
            slotList.append(slot)
    return slotList


#function: set_prof_priority
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


#function: prof_priority
#description: This function calculates and sets variables to be used in calculating the prof priority.
def prof_priority(prof, courses, index):
    requirements = [(courses.coursename in prof.courses), (len(prof.assignedCourses) <= 4)]
    reqSize = (len(requirements) - index)
    return all(requirements[:reqSize]), len(requirements[:reqSize])


#function: associate_priority_rooms
#description: This function associates possible rooms for courses based on a priority order.
def associate_priority_rooms(rooms, courses):
    #Prioritize ECS rooms first
    rooms.sort(key=lambda x: x.capacity, reverse = False)
    ecsRooms = [d for d in rooms if d.location[:3] == "ECS"]
    rooms =[d for d in rooms if d not in ecsRooms]
    rooms = ecsRooms + rooms
    
    courses.sort(key=lambda x: x.capacity, reverse = True)
    roomPossibilities = []
    for course in courses:
        possibilities = []
        for room in rooms:
            if course.type == "Lecture" or course.type is None:
                if(course.capacity <= room.capacity):
                    possibilities.append(room)
                
            else:
                if(30 <= room.capacity):
                    possibilities.append(room)
                
        roomPossibilities.append((course, possibilities))
    return roomPossibilities


#function: assign_rooms_all
#description: This function assigns the courses to their possible rooms based on a priority
#             by seats needed. If it can't match a course to a room the room attribute will
#             remain None.
def assign_rooms_all(courses, roomPossibilities):
  assignedRooms = []
  for k in range(len(courses)):
    for room in roomPossibilities[k][1]:
      if room not in assignedRooms:
        courses[k].room = room
        assignedRooms.append(room)
        break
    if courses[k].room == None:
      for room in roomPossibilities[k][1]:
         #find room where assigned
         index = 0
         for course in courses:
            if course.room == room:
               break
            else:
               index += 1
         #remove room from possibilities
         recursiveRoomPossibilities = deepcopy(roomPossibilities)
         roomIndex = 0
         for j in roomPossibilities[index][1]:
            if j == room:
               break
            else:
               roomIndex += 1
         del recursiveRoomPossibilities[index][1][roomIndex]

         #call function with new inputs
         saveCourses = deepcopy(courses)
         for course in courses:
            course.room = None
         assign_rooms_all(courses, recursiveRoomPossibilities)
         #if there is a course with no room continue loop with course's room as None
         for course in courses:
            if course.room == None:
               courses = deepcopy(saveCourses)
               continue
         #if no courses have a None room return the output
         return 


#function: assign_profs
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
#description: This function assigns rooms to courses, ensuring requirements are met.
def assign_rooms(courses, rooms):
    
    room = get_pref_room(rooms, courses)
    if room is not None:
        return room.location
    else: 
        return None


#function: get_pref_room
#description: This function selects a room to assign for a course.
def get_pref_room(rooms, courses):
    
    for room in rooms:
        if room.capacity >= courses.capacity:
            return room
        else:
            print("No valid room")
            return None


#function: lock_courses
#description: This function manually locks a course in a timeslot.
def lock_courses(inData):
    lockedPlacements = []
    for schedule in inData['lockedSchedule']:
        lockedPlacements.append(schedule)
    return lockedPlacements


#function: remove_locked_items
#description: This fuction removes redundant data. In the future, it should be adapted to 
#             account for any data that the system keeps that is recorded during other
#             functions, like how many classes a professor is currently listed to teach.
def remove_locked_items(inData):
    for schedule in inData['lockedSchedule']:
        for course in inData['courses']:
            if course['coursename'] == schedule['coursename']:
                inData['courses'].remove(course)
    return inData


#function: create_timeslots
#description: This function creates the global variable of all timeslots.
def create_timeslots(timeslots, Type):
    print(Type)
    for slots in timeslots:
        Week = {'Monday': None, 'Tuesday': None, 'Wednesday': None, 'Thursday': None, 'Friday': None}
        sortkey = None
        for day in slots.day:
            Week[day] = slots.startTimes
            if slots.startTimes is not None:
                sortkey = slots.startTimes
        globalTimeSlots[Type].append(TimeSlot(Week, Week, slots.length, sortkey))
    
    for i in range(len(globalTimeSlots[Type])):
        print(globalTimeSlots[Type][i].startTimes)


#function: assign_slots
#description: This function uses an algorithm to assign courses to timeslots based on a
#             weighted priority.
def assign_slots(course, prof, Type, formattedTimeslots):
  #for now just assigning at random and ignoring locked courses
  #this assumes by the time this function is called the courses will have all required data in their data type
  #for course in courses:
    #slot = random.randint(0,len(globalTimeSlots)-1)
    outDay = {}
    outLength = 50
    

    for slot in formattedTimeslots:
        key = list({ele for ele in slot.day if slot.day[ele]})[0]
        if (((Type == "Lab") and checkTimeslotOverlap(course, key, slot.day[key], slot.length, Type))
             or ((Type == "Tutorial") and checkTimeslotOverlap(course, key, slot.day[key], slot.length, Type))
             #or ((Type == "Lecture") and checkTimeslotOverlap(course, key, slot.day[key], slot.length, Type)))\
             or ((Type == "Lecture") and (len([i for i in course.noScheduleOverlap if i in [i[0] for i in slot.courses]]) == 0)))\
        and ((prof is None) or (prof not in slot.profs)):
            
            slot.courses.append((course.coursename, Type))
            slot.profs.append(prof)

            print("Timeslot: " + str([i[0] for i in slot.courses]))
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                if slot.startTimes[day] is not None:
                    outDay[day] = str(slot.startTimes[day].hour) + ":" + str(slot.startTimes[day].minute)
            print(outDay)
            break
        
    return outDay


#function: checkTimeslotOverlap
#description: This function checks if there is an overlap in timeslots.
def checkTimeslotOverlap(course, key, time, length, Type):

    allTimeSlots = globalTimeSlots['Lecture'] + globalTimeSlots['Lab'] + globalTimeSlots['Tutorial']

    numLabSlots = 5
    numTutorialSlots = 5
    if len(course.noScheduleOverlap) != 0:
        numLabSlots = 12/len(course.noScheduleOverlap)

    dateList = [d for d in allTimeSlots if ((key in d.day and d.day[key] is not None) and (d.day[key] >= (time - timedelta(minutes=d.length)) and d.day[key] < (time + timedelta(minutes=length))))]
    pass
    overLaps = 0
    for slot in dateList:
        if (Type == "Lab") and (([i[0] for i in slot.courses if (i[1] == "Lab")].count(course.coursename) >= math.ceil(course.labsNumber/numLabSlots)) or ([i[0] for i in slot.courses if (i[1] == "Lecture")].count(course.coursename) > 0)):
            overLaps += 1
        elif (Type == "Tutorial") and ([i[0] for i in slot.courses if (i[1] == "Tutorial")].count(course.coursename) >= math.ceil(course.tutorialsNumber/numLabSlots) or ([i[0] for i in slot.courses if (i[1] == "Lecture")].count(course.coursename) > 0)):
            overLaps += 1
        pass

        overLaps += len([i for i in (course.noScheduleOverlap) if i in [i[0] for i in slot.courses]])
        pass
    if overLaps == 0:
        return True
    else:
        return False

        
#function: get_in_data
#description: This function takes in the input data.
def get_in_data():
    f = open("recentData.json", "r")
    inDataJson = f.read()
    inData = json.loads(inDataJson)
    return inData


#function: create_out_data_dict
#description: This function creates the output dictionary.
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

#function: schedule_creation
#description: This is the main function for creating the schedule.
def schedule_creation(inData):
    
    outDataList = []

    #Parse out data that doesn't need to be scheduled, locked schedule components
    if 'lockedSchedule' in inData:
        outDataList = lock_courses(inData)
        inData = remove_locked_items(inData)

    courses = process_course_data(inData)

    courses.sort(key= lambda x: str(x.noScheduleOverlap))

    profs = process_prof_data(inData)
    rooms = process_room_data(inData)

    #print(json.dumps(inData, indent=4))
    #Scheduling Lectures
    Type = "Lecture"
    for course in courses:
        print("Scheduling: " + course.coursename)
        outData = create_out_data_dict()
        
        outData['coursename'] = course.coursename
        
        outData['professor'] = assign_profs(profs, course)

        if Type == "Lecture":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: len(x.courses), reverse=False)
            #formattedTimeslots = globalTimeSlots[Type]
        elif Type == "Lab" or Type == "Tutorial":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: (len(set(x.courses)), x.sortkey), reverse=False)
        else:
            formattedTimeslots = globalTimeSlots[Type]
        
        outData['starttime'] = assign_slots(course, outData['professor'], "Lecture", formattedTimeslots)
        
        
        
        #Base requirement all secheduled courses are lectures
        outData['type'] = "Lecture"
        
        outDataList.append(outData)


    slots = getAllTimeSlots(outDataList)

    for slot in slots:
        slotCourses = []
        roomCourses = []
        for course in outDataList:
            if course['starttime'] == slot:
                slotCourses.append(course)
        for course in slotCourses:
            for allCourses in courses:
                if allCourses.coursename == course['coursename']:
                    roomCourses.append(allCourses)


        roomPossibilities = associate_priority_rooms(rooms, roomCourses)
        assign_rooms_all(roomCourses, roomPossibilities)
        for course in roomCourses:
            for k in outDataList:
                if k['coursename'] == course.coursename:
                    k['room'] = str(course.room)

    #Special Case Monday Thursday Afternoons
    extraSlots = [x for x in slots if datetime.strptime(x[list(x.keys())[0]], "%H:%M") >= datetime.strptime("13:30", "%H:%M") and ("Monday" in list(x.keys()) or "Thursday" in list(x.keys()))]
    pass

    slotCourses = []
    roomCourses = []
    for course in outDataList:
        if course['starttime'] in extraSlots:
            slotCourses.append(course)
    for course in slotCourses:
        for allCourses in courses:
            if allCourses.coursename == course['coursename']:
                roomCourses.append(allCourses)

    #Special Case Tuesday Wednesday Friday Afternoons
    roomPossibilities = associate_priority_rooms(rooms, roomCourses)
    assign_rooms_all(roomCourses, roomPossibilities)
    for course in roomCourses:
        for k in outDataList:
            if k['coursename'] == course.coursename:
                k['room'] = str(course.room)

    extraSlots = [x for x in slots if datetime.strptime(x[list(x.keys())[0]], "%H:%M") >= datetime.strptime("13:30", "%H:%M") and ("Tuesday" in list(x.keys()) or "Wednesday" in list(x.keys()) or "Friday" in list(x.keys()))]
    pass

    slotCourses = []
    roomCourses = []
    for course in outDataList:
        if course['starttime'] in extraSlots:
            slotCourses.append(course)
    for course in slotCourses:
        for allCourses in courses:
            if allCourses.coursename == course['coursename']:
                roomCourses.append(allCourses)


    roomPossibilities = associate_priority_rooms(rooms, roomCourses)
    assign_rooms_all(roomCourses, roomPossibilities)
    for course in roomCourses:
        for k in outDataList:
            if k['coursename'] == course.coursename:
                k['room'] = str(course.room)

    pass
    #Scheduling Labs
    Type = "Lab"
    for course in courses:

        if Type == "Lecture":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: len(x.courses), reverse=False)
            #formattedTimeslots = globalTimeSlots[Type]
        elif Type == "Lab" or Type == "Tutorial":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: (len(set(x.courses)), x.sortkey), reverse=False)
        else:
            formattedTimeslots = globalTimeSlots[Type]

        for i in range(course.labsNumber):
            print("Scheduling Labs: " + course.coursename)
            outData = create_out_data_dict()
        
            outData['coursename'] = course.coursename

            outData['professor'] = None

            

            outData['starttime'] = assign_slots(course, None, "Lab", formattedTimeslots)
        
            outData['room'] = None

            outData['type'] = "Lab"
        
            outDataList.append(outData)


    
    #Scheduling Tutorials
    Type = "Tutorial"
    for course in courses:

        if Type == "Lecture":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: len(x.courses), reverse=False)
            #formattedTimeslots = globalTimeSlots[Type]
        elif Type == "Lab" or Type == "Tutorial":
            formattedTimeslots = sorted(globalTimeSlots[Type], key = lambda x: (len(set(x.courses)), x.sortkey), reverse=False)
        else:
            formattedTimeslots = globalTimeSlots[Type]

        for i in range(course.tutorialsNumber):
            print("Scheduling Tutorials: " + course.coursename)
            outData = create_out_data_dict()
        
            outData['coursename'] = course.coursename

            outData['professor'] = None

            outData['starttime'] = assign_slots(course, None, "Tutorial", formattedTimeslots)
        
            outData['room'] = None

            outData['type'] = "Tutorial"
        
            outDataList.append(outData)

    print("\nGenerated Schedule:\n" + json.dumps(outDataList, indent=4, default=jsonSerial))
    return outDataList


#function: jsonSerial
#description: This function is used for datetime string processing.
def jsonSerial(obj):
    if isinstance(obj, (datetime, date)):
        time = str(obj.hour) + ":" + str(obj.minute)
        return time
    raise TypeError ("Type %s is not serializable" % type(obj))


def main():
    #Clear globalTimeSlots
    globalTimeSlots['Lecture'] = []
    globalTimeSlots['Lab'] = []
    globalTimeSlots['Tutorial'] = []

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
