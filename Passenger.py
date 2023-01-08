import random

"""
Passenger class has a floor, a destination, an elevator, and a status
we can generate passengers by clicking a button on each floor and other attributes are randomly generated
the floor is an integer between 0 and 14
the destination is an integer between 0 and 14
the elevator is an elevator object
the status is either waiting, in elevator, or arrived
"""

class Passenger:
    def __init__(self, id, floor):
        self.id = id
        self.floor = floor
        self.destination = random.randint(0, 14)
        self.elevator = None
        self.status = "waiting"

    def __str__(self):
        return "Passenger " + str(self.id) + " is on floor " + str(self.floor) + " and wants to go to floor " + str(self.destination) + "."

    def get_direction(self):
        if self.floor < self.destination:
            return "up"
        elif self.floor > self.destination:
            return "down"
        else:
            return 0