#Floor class has a list of passengers, a list of elevators, and an id
#the id is an integer between 0 and 14
#the list of passengers is a list of passenger objects
#the list of elevators is a list of elevator objects
class Floor:
    def __init__(self, id):
        self.id = id
        self.passengers = []
        self.elevators = []