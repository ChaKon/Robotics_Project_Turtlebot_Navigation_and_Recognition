#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def Goal1():
    rospy.init_node('Goal1', anonymous=True)
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
    msg = Twist()
    r = rospy.Rate(10) # 10hz
    
    for x in range(1, 20):
        msg.linear.x= 0.5
        msg.angular.z= 0
        pub.publish(msg)
        r.sleep()
    for x in range(1, 68):
        msg.linear.x= 0
        msg.angular.z= 1
        pub.publish(msg)
        r.sleep()
    for x in range(1, 20):
        msg.linear.x= 0.5
        msg.angular.z= 0
        pub.publish(msg)
        r.sleep()
    msg.linear.x= 0
    msg.angular.z= 0
    pub.publish(msg)
    

if __name__ == '__main__':
    try:
        Goal1()
    except rospy.ROSInterruptException: pass
