""" 
classes that are used in the simulation => Elevator, Passenger, Floor, Building
Elevator class has a list of passengers, a status, a direction, and a floor, and a capacity
default floor is 0, default direction is NOT_MOVING, default status is idle, default capacity is 10
the direction is either UP, DOWN, or NOT_MOVING
the status is either idle, moving
the floor is an integer between 0 and 14
the capacity is an integer between 1 and 10
"""
class Elevator:
    def __init__(self, id):
        self.id = id + 1
        self.floor = 0
        self.direction = 0
        self.passengers = []
        self.capacity = 3
        self.speed = 1
        self.status = "idle"
        self.should_move = False
        self.target_flores = []

    def __str__(self):
        return "Elevator " + str(self.id) + " is on floor " + str(self.floor) + " and has " + str(len(self.passengers)) + " passengers."

    #TODO this function should be fixed 
    def move(self):
        if self.status == "moving":
            self.floor += self.direction * self.speed
            #TODO: change here
            #if elevator reaches one of the target floors in any index of target floors, remove it from the list
            if self.floor in self.target_flores:
                self.target_flores.remove(self.floor)
                if len(self.target_flores) == 0:
                    self.direction = 0
                    self.status = "idle"
                    self.should_move = False
            elif self.floor == 0:
                self.direction = 1
                if len(self.target_flores) > 0:
                    self.status = "moving"
                    self.should_move = True
            elif self.floor == 14:
                self.direction = -1
                if len(self.target_flores) > 0:
                    self.status = "moving"
                    self.should_move = True

        
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
        passenger.status = "arrived"
