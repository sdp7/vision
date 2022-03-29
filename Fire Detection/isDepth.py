#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import customDistance

#Gets the distance from the ros info and calls publish to publish things
def sonar_callback(self,data):
  	depth = data.field_of_view
	depthRange = false
	if depth < 2 and depth > 1:
		depthRange = True
	publish(depth,depthRange)

#Listens to the ros node and calls sonar_callback 
def listen():
	rospy.init_node('listener' ,anonymous=True)
	rospy.Subscriber("sonar1", <SonarType>, self.sonar_callback)
	rospy.spin()

#publishes if the fire is in range and the distance to the fire
def publish(depth, depthRange)
	rangepub = rospy.Publisher('isRange',customDistance)
	range = customDistance()
	range.inRange = depthRange
	range.depth = depth
	range.publish
if __name__ == '__main__':
listen()
