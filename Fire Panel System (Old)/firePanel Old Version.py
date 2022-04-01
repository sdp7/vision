from tkinter import *
import tkinter
from turtle import width
from datetime import date

class LED:
    def __init__(self, win, x0, x1, y0, y1):
        self.win = win
        self.lit = False
        self.circle = self.win.create_oval(x0, x1, y0, y1, fill="#18191A")

    def turn_on(self):
        self.win.itemconfig(self.circle, fill="green")
        self.lit = True

    def turn_off(self):
        self.win.itemconfig(self.circle, fill="#18191A")
        self.lit = False

#Turns the system off
def system_off():
    sys_on.config(state="normal")
    floor_input.config(state="normal")

    for x in [reset_button, raise_alert,fault_button, enter_button]:
        x.config(state="disabled")

    for x in [sys_name, sys_subname, group_name, date_label, location_label]:
        x.config(text="")

    if floor_input.get() != "":
        floor_input.delete(0,END)
        floor_input.config(state="disabled")

    LEDS["fire_led"].turn_off()
    LEDS["power_led"].turn_off()

#Turns the system on
def system_on():
    reset_button.config(state= "disabled")
    sys_on.config(state="disabled")

    raise_alert.config(state= "normal")
    fault_button.config(state= "normal")

    LEDS["power_led"].turn_on()

    sys_name.config(text="Buddy Fire System")
    sys_subname.config(text="Emulation")
    group_name.config(text="Designed by SDP Group 7")
    date_label.config(text= date.today().strftime("%d/%m/%Y"))

#Fire alarm
def alert():
    #window.after(5000) Adds delay
    reset_button.config(state="normal")

    for x in [sys_on, raise_alert, fault_button, floor_input, enter_button]:
        x.config(state= "disabled")

    LEDS["fire_led"].turn_on()
    location_label.config(text="Location : " + str(floor_input.get()))

#Trigger for fire alarm
def start_alert():
    floor_input.config(state="normal")
    enter_button.config(state="normal")
    fault_button.config(state= "disabled")

#Clear fault signal
def reset_fault():
    for x in [raise_alert, fault_button, sys_off]:
        x.config(state= "normal")

    LEDS["fault_led"].turn_off()
    fault_label.master.destroy
    fault_label.pack()

#Raise fault signal
def fault():
    global fault_label
    var.set(3)

    for x in [reset_button, sys_on, sys_off,  raise_alert, fault_button]:
        x.config(state="disabled")

    LEDS["fault_led"].turn_on()
    fault_label = Label(window, text="Fault Identified", bg="black", anchor= CENTER, fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    fault_label.place(x = 355, y = 325)

    window.after(10000,reset_fault)

#Resets the fire alarm
def reset():
    for x in [raise_alert, fault_button, floor_input]:
        x.config(state= "normal")

    floor_input.delete(0,END)

    for x in [reset_button, floor_input, enter_button]:
        x.config(state= "disabled")

    location_label.config(text= "")
    LEDS["fire_led"].turn_off()
    
if __name__ == "__main__":

    #Create relevant tinkter workspace
    window = tkinter.Tk(className=" Fire Panel Emulator")
    window.geometry("800x425")

    frame = tkinter.Frame(window)
    frame.pack()

    canvas = Canvas(window, width=800, height=425, bg="#3A3B3C")
    canvas.create_rectangle(250, 112, 570, 330, outline="black", fill="black")
    canvas.pack()

    #Assign relevant labels
    Label(window, text="FAULT", bg="#3A3B3C", fg="#FFFFFF", font=('Helvetica', 14, 'bold')).place(x = 84, y = 90)
    Label(window, text="FIRE", bg="#3A3B3C", width=8, anchor=E, fg="#FFFFFF", font=('Helvetica', 14, 'bold')).place(x = 628, y = 90)

    left_label_y = 140
    right_label_y = 140
    for x in ["Power Fault", "System Fault", "Delay", "Test", "Disablement"]:
        Label(window, text=x, bg="#3A3B3C", fg="#FFFFFF", font=('Helvetica', 14)).place(x = 84, y = left_label_y)
        left_label_y += 50

    for x in ["Verify", "Sounder", "Active", "Fault/Dis", "Power"]:
        Label(window, text=x, bg="#3A3B3C", width=8, anchor=E, fg="#FFFFFF", font=('Helvetica', 14)).place(x = 628, y = right_label_y)
        right_label_y += 50

    date_label = Label(window, text="", bg="black", fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    sys_name = Label(window, text="", bg="black", fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    sys_subname = Label(window, text="", bg="black", fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    group_name = Label(window, text="", bg="black", fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    location_label = Label(window, text="", bg="black", anchor= CENTER, fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
    
    date_label.place(x = 478, y = 145)
    sys_name.place(x = 334, y = 211)
    sys_subname.place(x = 368, y = 238)
    group_name.place(x = 310, y = 265)
    location_label.place(x = 342, y = 325)

    #Create LED lights
    LEDS = {}

    leds_x, leds_y = 65, 75
    for x in ["fault_led", "power_fault_led", "system_fault_led", "delay_led", "test_led", "disablement_led"]:
        LEDS[x] = LED(canvas, 62, leds_x, 72, leds_y)
        leds_x += 50
        leds_y += 50

    leds_x, leds_y = 65, 75
    for x in ["fire_led", "verify_led", "sounder_led", "active_led", "fault_dis_led", "power_led"]:
        LEDS[x] = LED(canvas, 725, leds_x, 735, leds_y)
        leds_x += 50
        leds_y += 50

    #Buttons
    var = IntVar()
    var.set(5)

    sys_on = Radiobutton(frame, text="System On",font=('Helvetica', 12), variable=var, value=1, command= system_on)
    reset_button = Radiobutton(frame, text="Reset",font=('Helvetica', 12), state= "disabled", variable=var, value=2, command= reset)
    fault_button = Radiobutton(frame, text="Fault",font=('Helvetica', 12), state= "disabled", variable=var, value=3, command= fault)
    raise_alert = Radiobutton(frame, text="Raise Alert",font=('Helvetica', 12), state= "disabled", variable=var, value=4, command= start_alert)
    sys_off = Radiobutton(frame, text="System Off",font=('Helvetica', 12), variable=var, value=5, command= system_off)
    enter_button = Button(frame,font=('Helvetica', 12),text="Enter",command= alert, state= "disabled")
    floor_input = tkinter.Entry(frame, state= "disabled")

    #Positioning of radio buttons and spaces
    sys_on.grid(row=10,column=1)
    sys_off.grid(row=10,column=2)
    reset_button.grid(row=10,column=3)
    fault_button.grid(row=10,column=4)
    raise_alert.grid(row=10,column=5)
    floor_input.grid(row=10, column=8)
    enter_button.grid(row=10, column=9)

    Label(frame, text="", width=6).grid(row=10,column=6)
    Label(frame, text="", width=2).grid(row=10,column=7)
    
    #Inititate output
    try:
        system_off()
        window.mainloop()
    except KeyboardInterrupt:
        system_off()
        window.destroy()