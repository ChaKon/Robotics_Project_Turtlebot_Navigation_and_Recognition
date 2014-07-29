#!/usr/bin/env python

import roslib; roslib.load_manifest('part1')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def GetPoint(Goal):
    global X
    global Y
    global FirstPoint
    if FirstPoint == 0: # Get the coordinate of the first goal published
        X = Goal.pose.position.x
        Y = Goal.pose.position.y
        FirstPoint = 1
        

def Waypoint(State):
    global WayPoint
    global X
    global Y
    GoalPub = rospy.Publisher('/move_base_simple/goal', PoseStamped)

   # Rotation
    if State.data == "State 4" :
        msg = PoseStamped()
        msg.header.frame_id = "map"  
       # Position 
        msg.pose.position.x = 0.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = 0.0        
       # Orientation 
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0 
        msg.pose.orientation.w = 0.0

        # Select the corect waypoint
        if WayPoint == 1:
            msg.pose.position.x = 3.5
            msg.pose.position.y = 1.5
            WayPoint = WayPoint + 1
        elif WayPoint == 2:
            msg.pose.position.x = 4.3
            msg.pose.position.y = 0.0
            WayPoint = WayPoint + 1
        elif WayPoint == 3:
            msg.pose.position.x = X
            msg.pose.position.y = Y
            WayPoint = 1

        
        rospy.sleep(2.0)
        GoalPub.publish(msg)
        
if __name__ == '__main__':
    try:
        WayPoint = 1
        FirstPoint = 0
        rospy.init_node('WayPoint')
        rospy.Subscriber("State", String, Waypoint)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, GetPoint)
	rospy.spin()

    except rospy.ROSInterruptException: 
        pass

