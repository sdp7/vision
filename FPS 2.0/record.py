import numpy as np
import cv2
import time
from datetime import datetime

capture_duration = 60
print("Hi, I am on")
cap = cv2.VideoCapture("http://abra:8080/?action=stream")

"""now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string = dt_string.replace("/","\\")"""

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('momo.avi',fourcc, 20.0, (640,480))

start_time = time.time()

try:
    while( int(time.time() - start_time) < capture_duration ):
        ret, frame = cap.read()
        out.write(frame)

    cap.release()
    out.release()
    print("Done")
except:
    cap.release()
    out.release()
    print("Error")
