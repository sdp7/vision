import cv2
from cv2 import blur
import numpy as np

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    blur_frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    
    contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    print(len(contours))

    key = cv2.waitKey(100)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()