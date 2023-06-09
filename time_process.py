#function: process_time_slots
#inputs: a string that holds the path of the time slot data
#outputs: an array of time slots of type TimeSlot
#description: This function processes the time slot data and returns it as a custom type
#             that can be processed by the algorithm.
def process_time_slots(str timeSlotsFilePath):
   class TimeSlot:
     def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

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

# Print the processed time slots
for slot in time_slots:
    print("Start time:", slot.start_time)
    print("End time:", slot.end_time)
    print()


#function: process_prof_data
#inputs: a string that holds the path of the prof data
#outputs: an array of type Prof
#description: This function processes the prof data and returns it as a custom type
#             that can be processed by the algorithm.
def process_prof_data(str profDataPath):
  class Prof:
    def __init__(self, name, department, office):
        self.name = name
        self.department = department
        self.office = office

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

# Print the processed professors
for professor in professors:
    print("Name:", professor.name)
    print("Department:", professor.department)
    print("Office:", professor.office)
    print()

#function: process_course_data
#inputs: a string that holds the path of the course data
#outputs: an array of type Course
#description: This function processes the course data and returns it as a custom type
#             that can be processed by the algorithm.
def process_course_data(str courseDataPath):
  class Course:
    def __init__(self, course_code, course_name, department):
        self.course_code = course_code
        self.course_name = course_name
        self.department = department

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
 # Print the processed courses
for course in course_list:
    print("Course Code:", course.course_code)
    print("Course Name:", course.course_name)
    print("Department:", course.department)
    print()
