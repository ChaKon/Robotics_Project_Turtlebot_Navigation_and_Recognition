#!/usr/bin/env python

import roslib; roslib.load_manifest('part1')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def callback(State):
    global rotation_number 
    global Rotation_End 

    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped)
    pub1 = rospy.Publisher('Rotation_End', String)

   # Rotation
    print(State.data)
    if State.data == "State 2" :
        print("Test")
        if rotation_number <= 4:
            msg = PoseStamped()
            msg.header.frame_id = "base_link"
          # Position
            msg.pose.position.x = 0.0
            msg.pose.position.y = 0.0
            msg.pose.position.z = 0.0
          # Orientation
            msg.pose.orientation.x = 0.0
            msg.pose.orientation.y = 0.0
            msg.pose.orientation.z = 0.5 # 90 degress on the left side
            msg.pose.orientation.w = 0.0

            Rotation_End = "False" 
            rospy.sleep(2.0)
            
            pub.publish(msg)
            
            pub1.publish(Rotation_End)
            rotation_number = rotation_number + 1
    
    elif (State.data == "State 3") and (rotation_number > 4):
        Rotation_End = "True"
        pub1.publish(Rotation_End)
    
    elif State.data == "State 6" :
        # Reset the Rotation during visual servoing
        rotation_number = 1
        Rotation_End = "False"
        
if __name__ == '__main__':
    try:
        rotation_number = 1
        Rotation_End = "False"
        rospy.init_node('rot')
        #rospy.init_node('Rotation_End')
        rospy.Subscriber("State", String, callback)
	rospy.spin()

    except rospy.ROSInterruptException: 
        pass

