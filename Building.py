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

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        passenger.elevator = self.choose_elevator_for_passenger(passenger)
        if passenger.elevator != None:
            passenger.elevator.add_passenger(passenger)
            passenger.status = "in elevator"
            print(passenger, "create successfully! ********in if")
        else:
            passenger.status = "waiting"
            passenger.direction = passenger.get_direction()
        self.floors[passenger.floor].passengers.append(passenger)
        print(passenger, "create successfully!")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        self.floors[passenger.floor].passengers.remove(passenger)

    def elevators_moving_update(self):
        # print(self.elevators[0].status, self.elevators[1].status, self.elevators[2].status)
        for elevator in self.elevators:
            if elevator.should_move and elevator.status == "moving" and len(elevator.target_flores) > 0:
                elevator.move()
                for passenger in elevator.passengers:
                    if passenger.destination == elevator.floor:
                        elevator.remove_passenger(passenger)
                        self.remove_passenger(passenger)
    
    def move_idle_elevator(self, elevator, floor, passenger):
        #move elevator to the floor
        if elevator.floor < floor.id:
            elevator.direction = 1
            elevator.should_move = True
            elevator.target_flores.append(floor.id)
            elevator.status = "moving"
        elif elevator.floor > floor.id:
            elevator.direction = -1
            elevator.should_move = True
            elevator.target_flores.append(floor.id)
            elevator.status = "moving"
        else:
            elevator.add_passenger(passenger)
            elevator.status = "moving"
            elevator.target_flores.append(passenger.destination)
            elevator.should_move = True
            if passenger.destination > passenger.floor:
                elevator.direction = 1
            elif passenger.destination < passenger.floor:
                elevator.direction = -1
            else:
                elevator.direction = 0
                elevator.status = "idle"
                elevator.should_move = False
            return

        return
    
    def floors_update(self):
        for floor in self.floors:
            for passenger in floor.passengers:
                # print(floor.id, passenger.status)
                if passenger.status == "waiting":
                    passenger.direction = passenger.get_direction()
                    # print(passenger.direction)
                    for elevator in self.elevators:
                        # print(elevator.status, passenger.direction)
                        if elevator.status == "idle":
                            self.move_idle_elevator(elevator, floor, passenger)
                            break
                            
    def update(self):
        self.elevators_moving_update()
        self.floors_update()
