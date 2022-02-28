import cv2
import numpy as np 
from PIL import Image
frame = cv2.imread("firebrick.jpg")
    # Converts images from BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower1 = np.array([0,100,20])
upper1 = np.array([10,255,255])
lower2 = np.array([160,100,20])
upper2 = np.array([179,255,255])
  
    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured 
    # objects found in the frame.
mask1 = cv2.inRange(hsv, lower1, upper1)
mask2 = cv2.inRange(hsv, lower2, upper2)
mask = mask1 + mask2

res = cv2.bitwise_and(frame,frame, mask= mask)
cv2.imshow('frame',frame)
cv2.imshow('mask',mask)
cv2.imshow('res',res)




#imgray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(mask,127,255,0)
M = cv2.moments(thresh)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


cv2.imshow('grey',frame)
cv2.waitKey(0)
	
   
  


  
