#The pseducode function for format Json action to take an input data and make a python dictionary
def FormatJson(inputJson):
    formattedJson = {}
import json

def ReadJsonFile(filename): # read the file 
    with open(filename, 'r') as file:
        json_data = file.read()
        python_dict = json.loads(json_data)
    return python_dict

#The pseducode function for the time slot abd rearrange the time schedule
def process_time_slots(path):
    time_slots = []
    
    # Read the time slot data from the file
    with open(path, 'r') as file:
        lines = file.readlines()
    
    # Process each line and create TimeSlot objects
    for line in lines:
        # Assuming each line contains start and end times separated by a comma
        start_time, end_time = line.strip().split(',')
        
        # Create a TimeSlot object and add it to the list
        time_slot = TimeSlot(start_time, end_time)
        time_slots.append(time_slot)
    
    return time_slots

# the array of time slots with their assigned data, a flag to indicate an impossible request
class TimeSlot:
    def __init__(self, start_time, end_time, data):
        self.start_time = start_time
        self.end_time = end_time
        self.data = data


def export_schedule(timeslots, isPossible):
    if isPossible:
        print("Cannot export schedule. This is an impossible request.")
        return

    schedule = []
    
    for timeslot in timeslots:
        slot_data = {
            "start_time": timeslot.start_time,
            "end_time": timeslot.end_time,
            "data": timeslot.data
        }
        schedule.append(slot_data)
    
    # Export schedule as JSON
    with open('schedule.json', 'w') as file:
        json.dump(schedule, file)

    print("Schedule exported successfully.")
    
#prefernece and location
class Prof:
    def __init__(self, name):
        self.name = name
class Course:
    def __init__(self, name):
        self.name = name
class Room:
    def __init__(self, name):
        self.name = name
class TimeSlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        
def check_possibility(profs, courses, rooms, banned_placements, locked_placements):
    # Add your logic to check if it is possible to generate a schedule
    # based on the provided data, banned placements, and locked placements
    # Return True if possible, False otherwise
    return True


def set_prof_priority(profs):
    # Add your logic to set the priority of professors
    # based on any relevant criteria
    # Modify the Prof objects or add an attribute to represent priority
    pass

# The dictionary would gp through the users data provided by Json to generate a schedule 
def GenerateSchedule(formattedJson):
    schedule = {}

    # Iterate over the key-value pairs in the formatted JSON
    for key, value in formattedJson.items():
        task_name = key
        task_duration = value

        # Add the task to the schedule
        schedule[task_name] = task_duration

    return schedule
