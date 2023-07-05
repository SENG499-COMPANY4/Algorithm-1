def check_schedule_overlap(course_a, course_b, course_c): 
#check the course in a b c and return the course does not conflict with each other in the time slots     
    conflict = False
    for course in [course_b, course_c]:
    #call for the course name check time to see whether it conflicts with each other or not
        if course['coursename'] in course_a['noScheduleOverlap']:
                conflict = True
                break

        return conflict

#give an example for the fourth year SUMMER: Taken all madatory course make sure it does not conflicts with each others
course_a = {
    "coursename": "SENG499",
    "noScheduleOverlap": ["SENG440", "SENG426"],
    "lecturesNumber": 1,
    "labsNumber": 2,
    "tutorialsNumber": 0,
    "capacity": 100
}

course_b = {
    "coursename": "SENG440",
    "noScheduleOverlap": ["SENG499", "SENG426"],
    "lecturesNumber": 1,
    "labsNumber": 0,
    "tutorialsNumber": 0,
    "capacity": 150
}

course_c = {
    "coursename": "SENG426",
    "noScheduleOverlap": ["SENG499", "SENG440"],
    "lecturesNumber": 1,
    "labsNumber": 0,
    "tutorialsNumber": 0,
    "capacity": 50
}

conflict = check_schedule_overlap(course_a, course_b, course_c)
print(conflict)  # Output: False (SENG499 does not conflict with SENG440 or SENG426)
