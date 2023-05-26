#The function for format Json action to take an input data and make a python dictionary

def FormatJson(inputJson):
    formattedJson = {}

    trimmedJson = inputJson.strip()

    if len(trimmedJson) == 0:
        return formattedJson

    if trimmedJson[0] != '{' or trimmedJson[-1] != '}':
        return formattedJson

    trimmedJson = trimmedJson[1:-1]

    keyValuePairs = trimmedJson.split(',')

    for pair in keyValuePairs:
        keyValue = pair.split(':')

        if len(keyValue) != 2:
            continue

        key = keyValue[0].strip()
        value = keyValue[1].strip()

        if key[0] != '"' or key[-1] != '"':
            continue

        key = key[1:-1]

        if value == 'null':
            formattedValue = None
        elif value == 'true':
            formattedValue = True
        elif value == 'false':
            formattedValue = False
        elif value[0] == '"' and value[-1] == '"':
            formattedValue = value[1:-1]
        elif value.isdigit():
            formattedValue = int(value)
        elif value.replace('.', '', 1).isdigit():
            formattedValue = float(value)
        else:
            continue

        formattedJson[key] = formattedValue

    return formattedJson

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
