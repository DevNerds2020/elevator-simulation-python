import tkinter as tk
from Building import Building
from Passenger import Passenger


"""
gui class has a building, a canvas, and a list of buttons
the building is a building object
the canvas is a tkinter canvas
the list of buttons is a list of tkinter buttons
"""
class GUI:
    def __init__(self, root):
        self.building = Building()
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="white")
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
            self.canvas.create_rectangle(100 * elevator.id + 50, 40 * (14 - elevator.floor) + 10, 100 * elevator.id + 90, 40 * (14 - elevator.floor) + 30, fill="white")
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
                elif(passenger.status == "arrived"):
                    #TODO: this here is not working properly
                    #beside of the red rectangle, put a green rectangle
                    self.canvas.create_rectangle(640, 40 * (14 - passenger.floor) + 10, 680, 40 * (14 - passenger.floor) + 30, fill="green")
                    #put a text in the rectangle that shows the number of passengers arrived
                    self.canvas.create_text(660, 40 * (14 - passenger.floor) + 20, text=str(len(floor.passengers)), anchor="w")

        lastMessages = self.building.messages[-25:]
        for message in lastMessages:
            messageIndex = lastMessages.index(message) + 1
            #put the messages in the right up side of canvas
            self.canvas.create_text(650, 20*messageIndex, text=message, anchor="w")
        self.building.update()
        root.after(1000, self.update)
root = tk.Tk()
gui = GUI(root)
root.mainloop()