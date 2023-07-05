def schedule_course(course, conflicting_courses, time_slots):
    conflict_exists = check_schedule_conflict(course, conflicting_courses, time_slots)

    if not conflict_exists:
        return True  # Course can be scheduled without conflicts

    # Reschedule the course
    available_time_slots = [slot for slot in time_slots if course not in slot.courses]

    for time_slot in available_time_slots:
        time_slot.courses.append(course)
        conflict_exists = schedule_course(course, conflicting_courses, time_slots)

        if not conflict_exists:
            return True  # Course rescheduled successfully without conflicts

        # Remove the course from the current time slot to try another one
        time_slot.courses.remove(course)

    return False  # Course cannot be scheduled without conflicts

# Example usage
course = "SENG 499"
conflicting_courses = ["SENG 440", "SENG 426"]

#Using the array of time slots called 'timeSlots'
schedule_success = schedule_course(course, conflicting_courses, timeSlots)

if schedule_success:
    print(f"{course} scheduled successfully without conflicts.")
else:
    print(f"Failed to schedule {course} due to conflicts.")
