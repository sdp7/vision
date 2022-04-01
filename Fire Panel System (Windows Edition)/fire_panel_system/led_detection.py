import cv2
import numpy as np

def detect(img, lower_range, upper_range):
    blur_frame = cv2.GaussianBlur(img, (5,5), 0)
    hsv_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv_frame, lower_range, upper_range)
    contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    return len(contours)