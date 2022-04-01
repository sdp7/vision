import pygetwindow as gw
import numpy as np
import pyautogui
import cv2
import tesseract
import led_detection
import system_update
import sys
from bs4 import *

def click_event(event, x,y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)

def determine_state(frame):

    ON = ['Buddy Fire System', 'Emulation', 'Designed by SDP Group 7']
    FIRE = "Location : "
    FAULT = "Fault"
    RESET = "Reset Fire Panel"
    location = ""
    fire_state = 0

    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])

    roi_screen = frame[214:392, 255:584]
    roi_fault_led = frame[116:151, 19:221]
    roi_power_led = frame[371:399, 586:799]
    roi_fire_led = frame[113:155, 583:801]

    screen = tesseract.text_detection(roi_screen)
    power_led = led_detection.detect(roi_power_led, lower_green, upper_green)
    fire_led = led_detection.detect(roi_fire_led, lower_green, upper_green)
    fault_led = led_detection.detect(roi_fault_led, lower_green, upper_green)

    if not(power_led) and not(fire_led) and not(fault_led) and screen == []:
        state = "SYS_OFF"
    elif power_led and screen == ON and not(fire_led) and not(fault_led):
        fire_state = 0
        state = "SYS_ON"
    elif power_led and not(fire_led) and screen[0:3] == ON  and RESET in screen[3]:
        state = "RESET"
    elif fire_led and power_led and screen[0:3] == ON and FIRE in screen[3]:
        fire_state = 1
        location = screen[3].replace(FIRE, "")
        state = "FIRE"
    elif power_led and fault_led and not(fire_led) and screen[0:3] == ON and FAULT in screen[3]:
        state = "FAULT"
    
    return state, (fire_state, location)

def update_server(state, location = ""):
    if state == "SYS_OFF":
        system_update.system_off()
    elif state == "RESET":
        system_update.reset_alarm()
    elif state == "SYS_ON":
        system_update.system_on()
    elif state == "FIRE":
        system_update.raise_alarm(location)
    elif state == "FAULT":
        system_update.raise_fault()

if __name__ == "__main__":

    window = gw.getWindowsWithTitle(" Fire Panel Emulator")[0]
    window.activate() 
    memory_state, memory_fire_state = "SYS_OFF", 0
    
    try:
        while window:
            img = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            current_state, (fire_state, location) = determine_state(frame)
            
            if memory_state != current_state:
                memory_state = current_state
                update_server(current_state, location)

            if fire_state != memory_fire_state:
                memory_fire_state = fire_state
                if fire_state == 1:
                    print("FIRE")
                else:
                    print("RESCUE")
    except:
        update_server("SYS_OFF")
        sys.exit()

        #cv2.imshow("screenshot", frame)
        #cv2.setMouseCallback("screenshot", click_event)
        #if cv2.waitKey(1) == ord("q"):
        #    break