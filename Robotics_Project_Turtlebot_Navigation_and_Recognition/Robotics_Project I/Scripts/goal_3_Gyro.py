#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu


def GetVal(data):
    global Z
    global W
    Z = data.orientation.z
    W = data.orientation.w

def callback(data):
    global Xstart
    global Ystart
    global Anglestart
    global Z
    global W
    global ini
    global Rangle
    global Rotupd
    
    acc = 1
    Goal = 1
    Speed = 0.4
    Rotation = 0.5
	
    msg = Twist()
    X = data.pose.pose.position.x
    Y = data.pose.pose.position.y
    #Z = data.pose.pose.orientation.z
    #W = data.pose.pose.orientation.w
    Angle = math.degrees(math.asin(Z)) * 2
	
    if ini == 0:
        Xstart = data.pose.pose.position.x
        Ystart = data.pose.pose.position.y
        Anglestart = Angle
        Rangle = Anglestart + 90
        Rotupd = 1
        ini = 1
        
    
    dt = math.sqrt(math.pow((math.fabs(X-Xstart)), 2) + math.pow((math.fabs(Y-Ystart)), 2))


	
    
    if Angle < 0:
        Angle = 360 + Angle
    elif Angle == 0 and (W == 0): #verif W
        Angle = 180
        
    print " dt = %2f" % dt
    print " Angle = %2f" % Angle
    print " Goal = %2f" % Goal
    print " Anglestart = %2f" % Anglestart 
    print " Rangle = %2f" % Rangle
    print "---------------------"
    if dt >= Goal:
        if Rangle > Angle - acc and Rangle < Angle + acc:
            Xstart = X
            Ystart = Y
            msg.linear.x = 0
            msg.angular.z = 0
            Rotupd = 0			
        else:
            if Rotupd == 0:
                Rangle = Rangle + 90
                if Rangle >= 360:
                    Rangle = Rangle - 360
                Rotupd = 1
                
            msg.linear.x = 0
            msg.angular.z = Rotation

    else:
        msg.linear.x = Speed
        msg.angular.z = 0

        #Anglestart = Angle
 
    pub.publish(msg)
  

def Goal3():
    global pub
    global Z
    global W    
    rospy.init_node('Goal3', anonymous=True)
    rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, GetVal)
    rospy.Subscriber("/odom", Odometry, callback)
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
    rospy.spin()

if __name__ == '__main__':
    try:
        ini = 0
        Goal3()
    except rospy.ROSInterruptException: pass
