#!/usr/bin/env python

import roslib; roslib.load_manifest('part1')
import roslib; roslib.load_manifest('ar_recog')
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from ar_recog.msg import Tags

def callback(data):
    global Dist
    global Y_rot
    Dist = data.tags[0].distance
    Y_rot = data.tags[0].yRot
    #print(data.tags[0].yRot) 
    servoing()
    
def CurrentState(data):
    global State
    State = data.data
    
    
def servoing():
    global Dist
    global Y_rot
    Speed = 0.3
    Rotation = 0.5
    Range = 0.015 
    Target_Range = 0.3
    msg = Twist()
    if 1 == 1:
        print(Dist)    
#if (State == "State 0"):
        if Y_rot >= 0 + Range:
            print("test")
            msg.linear.x = 0
            msg.angular.z = -Rotation	
        elif Y_rot <= 0 - Range:
            msg.linear.x = 0
            msg.angular.z = Rotation
        elif Dist >= Target_Range:
            msg.linear.x = Speed 
            msg.angular.z = 0
        else:
            msg.linear.x = 0
            msg.angular.z = 0
 
        pub.publish(msg)
        

if __name__ == '__main__':
    try:
        rospy.init_node('V_Ser', anonymous=True)
        rospy.Subscriber("tags", Tags, callback)
        rospy.Subscriber("State", String, CurrentState)        
        pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
        rospy.spin()
    except rospy.ROSInterruptException: pass
