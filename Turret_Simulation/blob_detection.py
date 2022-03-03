import cv2
from cv2 import blur
import numpy as np

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    blur_frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)
    
    lower_range_1 = np.array([0,100,20])
    upper_range_1 = np.array([10,255,255])
    #lower_range_2 = np.array([160,100,20])
    #upper_range_2 = np.array([179,255,255])
    
    lower_mask = cv2.inRange(hsv_frame, lower_range_1, upper_range_1)
    #upper_mask = cv2.inRange(hsv_frame, lower_range_2, upper_range_2)
    mask = lower_mask #+ upper_mask
    
    contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    (h, w) = frame.shape[:2]
    frame_center_x = w // 2
    frame_center_y = h // 2
    cv2.circle(frame, (w//2, h//2), 4, (255, 255, 255), -1) 

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 4000:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 2, (255, 255, 255), -1)

            change_x = cX - frame_center_x 
            change_y = frame_center_y - cY
            print(change_x, change_y)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(100)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()