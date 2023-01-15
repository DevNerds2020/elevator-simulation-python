from Floor import Floor
from Elevator import Elevator
from Passenger import Passenger
"""
in building class, we have a list of floors, a list of elevators, and a list of passengers
the list of floors is a list of floor objects
the list of elevators is a list of elevator objects
the list of passengers is a list of passenger objects
we have 15 floors, 3 elevators, and 0 passengers
"""
class Building:
    def __init__(self):
        self.floors = []
        self.elevators = []
        self.passengers = []
        self.messages = []
        for i in range(15):
            self.floors.append(Floor(i))
        for i in range(3):
            self.elevators.append(Elevator(i))

    def __str__(self):
        return "Building with " + str(len(self.floors)) + " floors, " + str(len(self.elevators)) + " elevators, and " + str(len(self.passengers)) + " passengers."

    def choose_elevator_for_passenger(self, passenger):
        for elevator in self.floors[passenger.floor].elevators:
            if elevator.status == "idle":
                return elevator
            elif elevator.status == "moving" and passenger.direction == "up" and elevator.direction == 1:
                return elevator
            elif elevator.status == "moving" and passenger.direction == "down" and elevator.direction == -1:
                return elevator
        return None

    def add_passenger_to_elevator(self, elevator, passenger):
        elevator.add_passenger(passenger)
        passenger.status = "in elevator"
        passenger.elevator = elevator
        elevator.target_flores.append(passenger.destination)
        self.remove_passenger(passenger)
        self.messages.append("Passenger " + str(passenger.id) + " is getting on elevator " + str(elevator.id) + " on floor " + str(passenger.floor) + " to go to floor " + str(passenger.destination) + ".")

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        passenger.elevator = self.choose_elevator_for_passenger(passenger)
        passenger.status = "waiting"
        passenger.direction = passenger.get_direction()
        self.floors[passenger.floor].passengers.append(passenger)
        self.messages.append("Passenger " + str(passenger.id) + " is waiting on floor " + str(passenger.floor) + " to go to floor " + str(passenger.destination) + ".")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        self.floors[passenger.floor].passengers.remove(passenger)

    def update_moving_elevators(self):
        for elevator in self.elevators:
            if elevator.should_move and elevator.status == "moving" and len(elevator.target_flores) > 0:
                elevator.move()
                for passenger in elevator.passengers:
                    if passenger.destination == elevator.floor:
                        elevator.remove_passenger(passenger)
                        self.messages.append("Passenger " + str(passenger.id) + " arrived at floor " + str(passenger.destination) + ". with elevator " + str(elevator.id) + ".")
                for passenger in self.floors[elevator.floor].passengers:
                    if passenger.status == "waiting" and elevator.capacity > len(elevator.passengers):
                        if ( elevator.direction == -1 and passenger.direction == "down" ) or ( elevator.direction == 1 and passenger.direction == "up" ):
                            self.add_passenger_to_elevator(elevator, passenger)
                        

    def choose_elevator_direction(self, elevator, floor, passenger):
        if elevator.floor < floor.id:
            elevator.target_flores.append(floor.id)
            elevator.direction = 1
        elif elevator.floor > floor.id:
            elevator.target_flores.append(floor.id)
            elevator.direction = -1
        else:
            while len(elevator.passengers) < 3 and len(floor.passengers) > 0:
                self.add_passenger_to_elevator(elevator, floor.passengers[0])
            if passenger.destination > passenger.floor:
                elevator.direction = 1
            elif passenger.destination < passenger.floor:
                elevator.direction = -1
            else:
                elevator.direction = 0
                elevator.status = "idle"
                elevator.should_move = False
            return

    #move elevator to the floor
    def move_idle_elevator(self, elevator, floor, passenger):
        elevator.should_move = True
        elevator.status = "moving"
        self.choose_elevator_direction(elevator, floor, passenger)
        return
    
    # floor update is looking for waiting passengers and is finding idle elevators to send them to the passengers
    def update_idle_elevators(self):
        for floor in self.floors:
            for passenger in floor.passengers:
                if passenger.status == "waiting":
                    passenger.direction = passenger.get_direction()
                    # print(passenger.direction)
                    for elevator in self.elevators:
                        # print(elevator.status, passenger.direction)
                        if elevator.status == "idle":
                            self.move_idle_elevator(elevator, floor, passenger)
                            break 

    # our main loop is always running and checking the moving and waiting elevators                        
    def update(self):
        self.update_moving_elevators()
        self.update_idle_elevators()