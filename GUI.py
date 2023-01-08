
from time import sleep
import tkinter as tk
from Building import Building
from Passenger import Passenger
from Elevator import Elevator
from Floor import Floor

"""
gui class has a building, a canvas, and a list of buttons
the building is a building object
the canvas is a tkinter canvas
the list of buttons is a list of tkinter buttons
"""
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
        self.canvas.delete("all")
        for i in range(15):
            self.canvas.create_line(0, 40 * i, 600, 40 * i, fill="black")
            self.canvas.create_text(20, 40 * i + 20, text=str(14 - i), anchor="w")
        for elevator in self.building.elevators:
            self.canvas.create_rectangle(100 * elevator.id + 50, 40 * (14 - elevator.floor) + 10, 100 * elevator.id + 90, 40 * (14 - elevator.floor) + 30, fill="blue")
            for passenger in elevator.passengers:
                #put a red text in the rectangle that shows the number of passengers in the elevator
                self.canvas.create_text(100 * elevator.id + 70, 40 * (14 - elevator.floor) + 20, text=str(len(elevator.passengers)), fill="red", anchor="w")
        for floor in self.building.floors:
            for passenger in floor.passengers:
                if(passenger.status == "waiting"):
                    #check the elevators status and send the nearest one
                    self.canvas.create_rectangle(600, 40 * (14 - passenger.floor) + 10, 640, 40 * (14 - passenger.floor) + 30, fill="red")
                    #put a text in the rectangle that shows the number of passengers waiting
                    self.canvas.create_text(620, 40 * (14 - passenger.floor) + 20, text=str(len(floor.passengers)), anchor="w")
                    # self.building.check_elevators_for_sending_to_floor_and_send(passenger.floor)
                #TODO
                # elif(passenger.status == "in elevator"):
                #     #rectangle has a text in it that shows the number of passengers in the elevator
                #     # create a text in the rectangle that shows the number of passengers in the elevator
                #     self.canvas.create_text(620, 40 * (14 - passenger.floor) + 20, text=str(len(passenger.elevator.passengers)), anchor="w")
                #     #create a rectangle that shows the number of passengers in the elevator
                #     self.canvas.create_rectangle(600, 40 * (14 - passenger.floor) + 10, 640, 40 * (14 - passenger.floor) + 30, fill="blue")
        self.building.update()
        root.after(100, self.update)
root = tk.Tk()
gui = GUI(root)
root.mainloop()