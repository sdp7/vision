#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64MultiArray, Bool
import cv2
import numpy as np
#import imutils
import os
cur = os.path.dirname(os.path.realpath(__file__))


class FireDetector:
    def __init__(self):
        rospy.init_node('isFire')
        self.capture = cv2.VideoCapture('http://abra:8080/?action=stream')
        self.rate = rospy.Rate(20)
        self.pub1 = rospy.Publisher("isFire", Bool, queue_size=10)
        self.pub2 = rospy.Publisher("fire_pos", Float64MultiArray, queue_size=10)
        onx_path = cur + "/best.onnx"
        print(f"this is where onx files is {onx_path}")
        self.net = cv2.dnn.readNet(onx_path)
        self.colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]
        self.counter = 0
        self.isFire = False

        self.statepub = rospy.Publisher('scan_state', Bool, queue_size =10)

    #Find Fires    
    def unwrap_detection(self,input_image, output_data):
        class_ids = []
        confidences = []
        boxes = []

        rows = output_data.shape[0]
        
        _,_, image_width, image_height = input_image.shape
    
        x_factor = image_width / 640
        y_factor =  image_height / 640

        for r in range(rows):
            row = output_data[r]
            confidence = row[4]
            if confidence >= 0.6:

                classes_scores = row[5:]
                _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
                class_id = max_indx[1]
                if (classes_scores[class_id] > .25):

                    confidences.append(confidence)

                    class_ids.append(class_id)

                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item() 
                    left = int((x - 0.5 * w) * x_factor)
                    top = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)

        return class_ids, confidences, boxes
    
    # Format the frame
    def format_yolov5(self, source):
        #print(source.shape)	
        # put the image in square big enough
        col, row, _ = source.shape
        _max = max(col, row)
        resized = np.zeros((_max, _max, 3), np.uint8)
        resized[0:col, 0:row] = source
    
        # resize to 640x640, normalize to [0,1[ and swap Red and Blue channels
        result = cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)
        return result

    # the output will be written to output.avi
    global out
    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.0,(640,640))
    
    #This should publish the coordinates of the fire (specifically the base of the fire)
    def publish(self):
        ret,frame = self.capture.read()
        shapedframe = self.format_yolov5(frame)
        self.net.setInput(shapedframe)
        outs = self.net.forward()
        class_ids, confidences, boxes = self.unwrap_detection(shapedframe, outs[0])
        CoordMsg = Float64MultiArray()
        
        if len(boxes) != 0:
                mainFire = np.argmax(confidences)
                mainFireLoc = boxes[mainFire]
                CentreX = mainFireLoc[0] + mainFireLoc[2]
                CentreY = mainFireLoc[1] - mainFireLoc[3]
                CoordMsg.data.append(CentreX)
                CoordMsg.data.append(CentreY)
                CoordMsg.data.append(mainFireLoc[2])
                self.isFire = True
                self.pub1.publish(self.isFire)
                self.pub2.publish(CoordMsg)
                self.statepub.publish(False)
                # exit()
        
        else: 
            # self.isFire = False
            self.pub2.publish(CoordMsg)
            # self.statepub.publish(True)
            self.pub1.publish(self.isFire)
    
	
        # For Printing out Fire
        # for (classid, confidence, box) in zip(class_ids, confidences, boxes):
        #      	color = self.colors[int(classid) % len(self.colors)]
        #      	cv2.rectangle(frame, box, color, 2)
        #      	cv2.rectangle(frame, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
        #      	cv2.putText(frame, 'fire', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))
        # cv2.imshow("output", frame)
        # cv2.waitKey(1)

if __name__ == '__main__':
    F = FireDetector()
    # statepub = rospy.Publisher('scan_state', Bool, queue_size =10)
    # statepub.publish(True) 
    while not rospy.is_shutdown():
        try:
            F.publish()
            F.rate.sleep()
            k = cv2.waitKey(25)
            if k == 27:
                break
        except rospy.ROSInterruptException:
            print("Shutting down")
            break
    
    cv2.destroyAllWindows()


