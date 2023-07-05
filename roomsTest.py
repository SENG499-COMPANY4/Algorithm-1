#class: Room
#building: building code of room
#number: room number
#capacity: max seats
#hastech: bool for if room equipped for connecting technology
class Room:
  def __init__(self, building, number, capacity, hasTech):
    self.building = building
    self.number = number
    self.capacity = capacity
    self.hasTech = hasTech

  def __str__(self):
    return self.building + self.number

#class: Course
#coursename: the name of the course
#lecturesNumber: 
#labsNumber: 
#tutorialsNumber: 
#capacity: 
class Course:
  def __init__(self, coursename, lecturesNumber, labsNumber, tutorialsNumber, capacity, needsTech, room):
    self.coursename = coursename
    self.lecturesNumber = lecturesNumber
    self.labsNumber = labsNumber
    self.tutorialsNumber = tutorialsNumber
    self.capacity = capacity
    self.needsTech = needsTech
    self.room = room

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

def assign_rooms(courses, roomPossibilities):
  assignedRooms = []
  for k in range(len(courses)):
    for room in roomPossibilities[k][1]:
      if room not in assignedRooms:
        courses[k].room = room
        assignedRooms.append(room)
        break


    

def main():
    rooms = [Room("AAA", "111", 250, True), Room("AAA", "333", 50, True), Room("BBB", "111", 250, False), Room("BBB", "222", 100, True), Room("CCC", "111", 150, True), Room("AAA", "222", 50, False)]
    courses = [Course("A", 3, 0, 0, 50, True, None), Course("B", 3, 0, 0, 150, False, None), Course("C", 3, 0, 0, 250, True, None), Course("D", 3, 0, 0, 250, True, None)]
    roomPossibilities = associate_priority_rooms(rooms, courses)
    for t in roomPossibilities:
        print(t[0].coursename)
        for y in t[1]:
            print(str(y))
    assign_rooms(courses, roomPossibilities)
    for course in courses:
      print(course.coursename)
      print(course.room)

if __name__ == "__main__":
    main()
