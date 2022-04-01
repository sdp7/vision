import numpy as np
import cv2
import time
from datetime import datetime
import urllib.request

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string = dt_string.replace("/","")
dt_string = dt_string.replace(":","")

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(dt_string + ".avi",fourcc, 20.0, (640,480))

stream = urllib.request.urlopen("http://abra:8080/?action=stream")
bytes = b''

try:

    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8') #frame starting 
        b = bytes.find(b'\xff\xd9') #frame ending
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            out.write(img)

    cap.release()
    out.release()
    print("Success")
except:
    cap.release()
    out.release()
    print("Error")
