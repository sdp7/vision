import numpy as np
import cv2
from datetime import datetime
capture = cv2.VideoCapture(0)  
  
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
"""now = date.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string.replace(" ","_")
print(now)"""
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (640, 480))
  
while(True):
    ret, frame = capture.read() 
    out.write(frame) 

    cv2.imshow('Original', frame)
      
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
  

capture.release()
out.release() 
  
cv2.destroyAllWindows()