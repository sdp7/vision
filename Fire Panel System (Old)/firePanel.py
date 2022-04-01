from glob import glob
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
    global reset_button, raise_alert, floor_input, sys_on
    sys_on.config(state="normal")
    reset_button.config(state="disabled")
    raise_alert.config(state="disabled")
    floor_input.config(state="disabled")
    led_reset()
    Label(window, text="", width=9, bg="black", fg="#FFFFFF").place(x = 380, y = 100)
    Label(window, text="", width=6, bg="black", fg="#FFFFFF", font=('Helvetica', 40, 'bold')).place(x = 220, y = 160)
    Label(window, text="", width=18, bg="black", fg="#FFFFFF").place(x = 247, y = 250)
    if floor_input.get() != "":
        floor_input.config(state="normal")
        floor_input.delete(0,END)

#Turn all the leds off
def led_reset():
    global LEDS
    for led in LEDS.keys():
        if LEDS[led].lit == True: LEDS[led].turn_off()

#Turns the system on
def system_on():
    global LEDS, reset_button, raise_alert
    reset_button.config(state= "disabled")
    raise_alert.config(state= "normal")
    led_reset()
    LEDS["power_led"].turn_on()
    today = date.today().strftime("%d/%m/%Y")
    Label(window, text=today, bg="black", fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 380, y = 100)
    Label(window, text="Buddy Fire System", bg="black", fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 243, y = 160)
    Label(window, text="Emulation", bg="black", fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 272, y = 180)
    Label(window, text="Designed by SDP Group 7", bg="black", fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 222, y = 200)
    
#Triggers a fire alarm
def alert():
    global LEDS, floor_input, sys_on
    #window.after(10000) Adds delay
    sys_on.config(state="disabled")
    floor_input.config(state="disabled")
    system_on()
    reset_button.config(state="normal")
    LEDS["fire_led"].turn_on()
    Label(window, text="Location : Floor " + floor_input.get(), width=14, bg="black", anchor= CENTER, fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 247, y = 250)

#Resets the fire alarm
def reset():
    global LEDS
    system_on()
    Label(window, text="", width=18, bg="black", anchor= CENTER, fg="#FFFFFF").place(x = 247, y = 250)
    if floor_input.get() != "":
        floor_input.config(state="normal")
        floor_input.delete(0,END)
    
if __name__ == "__main__":

    #Create relevant tinkter workspace
    window = tkinter.Tk(className=" Fire Panel Emulator")
    window.geometry("600x300")

    frame = tkinter.Frame(window)
    frame.pack()

    canvas = Canvas(window, width=600, height=300, bg="#3A3B3C")
    canvas.create_rectangle(160, 70, 450, 250, outline="black", fill="black")
    canvas.pack()

    #Assign relevant labels
    Label(window, text="FAULT", bg="#3A3B3C", fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 43, y = 55)
    Label(window, text="FIRE", bg="#3A3B3C", width=6, anchor=E, fg="#FFFFFF", font=('Helvetica', 10, 'bold')).place(x = 500, y = 55)

    left_label_y = 95
    right_label_y = 95
    for x in ["Power Fault", "System Fault", "Delay", "Test", "Disablement"]:
        Label(window, text=x, bg="#3A3B3C", fg="#FFFFFF", font=('Helvetica', 10)).place(x = 43, y = left_label_y)
        left_label_y += 40

    for x in ["Verify", "Sounder", "Active", "Fault/Dis", "Power"]:
        Label(window, text=x, bg="#3A3B3C", width=6, anchor=E, fg="#FFFFFF", font=('Helvetica', 10)).place(x = 500, y = right_label_y)
        right_label_y += 40

    #Create LED lights
    LEDS = {}

    leds_x, leds_y = 35, 45
    for x in ["fault_led", "power_fault_led", "system_fault_led", "delay_led", "test_led", "disablement_led"]:
        LEDS[x] = LED(canvas, 23, leds_x, 33, leds_y)
        leds_x += 40
        leds_y += 40

    leds_x, leds_y = 35, 45
    for x in ["fire_led", "verify_led", "sounder_led", "active_led", "fault_dis_led", "power_led"]:
        LEDS[x] = LED(canvas, 565, leds_x, 575, leds_y)
        leds_x += 40
        leds_y += 40

    #Buttons
    var = IntVar()
    var.set(4)

    sys_on = Radiobutton(frame, text="System On", variable=var, value=1, command= system_on)
    reset_button = Radiobutton(frame, text="Reset", state= "disabled", variable=var, value=2, command= reset)
    raise_alert = Radiobutton(frame, text="Raise Alert", state= "disabled", variable=var, value=3, command= lambda: floor_input.config(state="normal"))
    sys_off = Radiobutton(frame, text="System Off", variable=var, value=4, command= system_off).grid(row=10,column=2)
    button = Button(frame,text="Enter",command= alert).grid(row=10, column=8)
    floor_input = tkinter.Entry(frame, state= "disabled")

    #Positioning of radio buttons and spaces
    sys_on.grid(row=10,column=1)
    reset_button.grid(row=10,column=3)
    raise_alert.grid(row=10,column=4)
    floor_input.grid(row=10, column=6)

    Label(frame, text="", width=6).grid(row=10,column=5)
    Label(frame, text="", width=2).grid(row=10,column=7)
    
    window.mainloop()