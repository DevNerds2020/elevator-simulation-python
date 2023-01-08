""" 
classes that are used in the simulation => Elevator, Passenger, Floor, Building
Elevator class has a list of passengers, a status, a direction, and a floor, and a capacity
default floor is 0, default direction is NOT_MOVING, default status is idle, default capacity is 10
the direction is either UP, DOWN, or NOT_MOVING
the status is either idle, moving, or full
the floor is an integer between 0 and 14
the capacity is an integer between 1 and 10
"""
class Elevator:
    def __init__(self, id):
        self.id = id
        self.floor = 0
        self.direction = 0
        self.passengers = []
        self.capacity = 10
        self.speed = 1
        self.status = "idle"
        self.should_move = False
        self.target_flores = []

    def __str__(self):
        return "Elevator " + str(self.id) + " is on floor " + str(self.floor) + " and has " + str(len(self.passengers)) + " passengers."

    def move(self):
        if self.status == "moving":
            self.floor += self.direction * self.speed
            # print("self.floor = " + str(self.floor))
            # print("self.target_flores[0] = " + str(self.target_flores[0]))
            if self.floor == self.target_flores[0]:
                self.target_flores.pop(0)
                if len(self.target_flores) == 0:
                    self.direction = 0
                    self.status = "idle"
                    self.should_move = False
                    print("elevator reached destination")
                else:
                    if self.floor < self.target_flores[0]:
                        self.direction = 1
                        self.status = "moving"
                    elif self.floor > self.target_flores[0]:
                        self.direction = -1
                        self.status = "moving"
                    else:
                        self.direction = 0
                        self.status = "idle"
                        self.should_move = False
            elif self.floor == 0:
                self.direction = 0
                self.status = "idle"
            elif self.floor == 14:
                self.direction = 0
                self.status = "idle"


        
    def add_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            passenger.elevator = self
            passenger.status = "in elevator"
            return True
        else:
            return False

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        passenger.elevator = None
        passenger.status = "waiting"
