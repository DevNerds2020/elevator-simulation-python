from time import sleep
import tkinter as tk
import random

#function to move the elevator   self.building.elevators[0].move_to_floor(13)

# classes that are used in the simulation => Elevator, Passenger, Floor, Building
#Elevator class has a list of passengers, a status, a direction, and a floor, and a capacity
#default floor is 0, default direction is NOT_MOVING, default status is idle, default capacity is 10
# the direction is either UP, DOWN, or NOT_MOVING
# the status is either idle, moving, or full
# the floor is an integer between 0 and 14
# the capacity is an integer between 1 and 10
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

    def move_to_floor(self, floor):
        # print("self.floor = " + str(self.floor))
        # print("moving to floor " + str(floor))
        if self.floor < floor:
            self.direction = 1
            self.status = "moving"
        elif self.floor > floor:
            self.direction = -1
            self.status = "moving"
        else :
            self.direction = 0
            self.status = "idle"
            self.should_move = False
        
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

#Passenger class has a floor, a destination, an elevator, and a status
#we can generate passengers by clicking a button on each floor and other attributes are randomly generated
#the floor is an integer between 0 and 14
#the destination is an integer between 0 and 14
#the elevator is an elevator object
#the status is either waiting, in elevator, or arrived
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

#Floor class has a list of passengers, a list of elevators, and an id
#the id is an integer between 0 and 14
#the list of passengers is a list of passenger objects
#the list of elevators is a list of elevator objects
class Floor:
    def __init__(self, id):
        self.id = id
        self.passengers = []
        self.elevators = []

# in building class, we have a list of floors, a list of elevators, and a list of passengers
# the list of floors is a list of floor objects
# the list of elevators is a list of elevator objects
# the list of passengers is a list of passenger objects
# we have 15 floors, 3 elevators, and 0 passengers
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
    def update(self):
        # print('update')
        for elevator in self.elevators:
            # print(elevator.floor, elevator.status, elevator.direction, elevator.should_move, elevator.target_flores)
            if elevator.should_move and elevator.status == "moving" and len(elevator.target_flores) > 0:
                elevator.move()
                for passenger in elevator.passengers:
                    if passenger.destination == elevator.floor:
                        elevator.remove_passenger(passenger)
                        self.remove_passenger(passenger)
        for floor in self.floors:
            for passenger in floor.passengers:
                # print(floor.id, passenger.status)
                if passenger.status == "waiting":
                    passenger.direction = passenger.get_direction()
                    # print(passenger.direction)
                    for elevator in self.elevators:
                        # print(elevator.status, passenger.direction)
                        if elevator.status == "idle":
                            #move elevator to the floor
                            if elevator.floor < floor.id:
                                elevator.direction = 1
                            elif elevator.floor > floor.id:
                                elevator.direction = -1
                            else:
                                elevator.add_passenger(passenger)
                                self.remove_passenger(passenger)
                                elevator.status = "moving"
                                elevator.should_move = True
                                if passenger.destination > passenger.floor:
                                    elevator.direction = 1
                                elif passenger.destination < passenger.floor:
                                    elevator.direction = -1
                                else:
                                    elevator.direction = 0
                                    elevator.remove_passenger(passenger)
                                    self.add_passenger(passenger)
                                return
                            elevator.should_move = True
                            elevator.target_flores.append(floor.id)
                            elevator.status = "moving"
                            return
#gui class has a building, a canvas, and a list of buttons
#the building is a building object
#the canvas is a tkinter canvas
#the list of buttons is a list of tkinter buttons
class GUI:
    def __init__(self, root):
        self.building = Building()
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        self.buttons = []
        for i in range(15):
            #buttons should be beside each floor
            self.buttons.append(tk.Button(root, text="Call elevator on floor " + str(14-i), command=lambda i=i: self.building.add_passenger(Passenger(id = len(self.building.passengers), floor = 14-i))))
            #put the buttons aside of each floor
            self.buttons[i].pack()
            #buttons should be beside each floor
            self.buttons[i].place(x=600, y=40 * i)
        self.update()

    def update(self):
        # self.building.elevators[0].move_to_floor(13)
        self.canvas.delete("all")
        for i in range(15):
            self.canvas.create_line(0, 40 * i, 600, 40 * i, fill="black")
            self.canvas.create_text(20, 40 * i + 20, text=str(14 - i), anchor="w")
        for elevator in self.building.elevators:
            self.canvas.create_rectangle(100 * elevator.id + 50, 40 * (14 - elevator.floor) + 10, 100 * elevator.id + 90, 40 * (14 - elevator.floor) + 30, fill="blue")
            for passenger in elevator.passengers:
                self.canvas.create_rectangle(100 * elevator.id + 50, 40 * (14 - passenger.floor) + 10, 100 * elevator.id + 90, 40 * (14 - passenger.floor) + 30, fill="red")
        for floor in self.building.floors:
            for passenger in floor.passengers:
                if(passenger.status == "waiting"):
                    #check the elevators status and send the nearest one
                    self.canvas.create_rectangle(600, 40 * (14 - passenger.floor) + 10, 640, 40 * (14 - passenger.floor) + 30, fill="red")
                    #put a text in the rectangle that shows the number of passengers waiting
                    self.canvas.create_text(620, 40 * (14 - passenger.floor) + 20, text=str(len(floor.passengers)), anchor="w")
                    # self.building.check_elevators_for_sending_to_floor_and_send(passenger.floor)
                elif(passenger.status == "in elevator"):
                    #rectangle has a text in it that shows the number of passengers in the elevator
                    self.canvas.create_rectangle(100 * passenger.elevator.id + 50, 40 * (14 - passenger.floor) + 10, 100 * passenger.elevator.id + 90, 40 * (14 - passenger.floor) + 30, fill="red")
                    #put a text in the rectangle that shows the number of passengers in the elevator
                    self.canvas.create_text(100 * passenger.elevator.id + 70, 40 * (14 - passenger.floor) + 20, text=str(len(passenger.elevator.passengers)), anchor="w")
        self.building.update()
        root.after(100, self.update)
    
root = tk.Tk()
gui = GUI(root)
root.mainloop()