#The pseducode function for format Json action to take an input data and make a python dictionary
def FormatJson(inputJson):
    formattedJson = {}
import json

def ReadJsonFile(filename):
    with open(filename, 'r') as file:
        json_data = file.read()
        python_dict = json.loads(json_data)
    return python_dict


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
