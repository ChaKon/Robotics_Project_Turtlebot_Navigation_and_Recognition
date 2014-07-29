#!/usr/bin/env python

import roslib; roslib.load_manifest('part1')
import roslib; roslib.load_manifest('ar_recog')
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped
from ar_recog.msg import Tags, Tag


def ImuVal(data):
    global Z
    global RobotNotMoving
    global Stuck
    Zprev = Z
    Z = data.orientation.z
    Seq = data.header.seq
    if Z == Zprev:
        # Time difference between last movement and actual time
        if Stuck + 200 <= Seq:
            RobotNotMoving = 1 # True
            Stuck = Seq # Reset Counter
            State()
    else:
        Stuck = Seq # Reset Counter
        RobotNotMoving = 0 # False

    


def Target(data):
    global TargetDetect
    print(data.tag_count)
    if data.tag_count >= 0:
        TargetDetect = 1
        State()
    else:
        TargetDetect = 0
        State()
    
        
def callback_ST0(data):
    global CurrentState
    global Goal_pub
    global GoalNb
    PrevGoalNb = GoalNb
    GoalNb = data.header.seq
    if PrevGoalNb != GoalNb: # New goal publish
        Goal_pub = 1
    else:
        Goal_pub = 0
    print(Goal_pub)
    State()
    
def RotEnd(data):
    global RotationOver
    # Get the flag for rotation status
    if data.data == "False":
        RotationOver = 0
    elif data.data == "True":
        RotationOver = 1
    State()



def State():
    global CurrentState
    global Goal_pub
    global RobotNotMoving
    global RobotRotation
    global RotationOver
    global TargetDetect
    
    pub = rospy.Publisher('State', String)
    

    # if Target detected go to State 6 
    if ( CurrentState != "State 0" ) or ( CurrentState != "State 1" ): # Visual Servoing    
        if TargetDetect == 1:
            CurrentState = "State 6" 
            
    if CurrentState == "State 0":  #ini
        if Goal_pub == 1: # New Goal publish
            CurrentState = "State 1"
            
    elif CurrentState == "State 1": # 1st goal reach
        # Target reach or Robot stuck
        if RobotNotMoving == 1:
            CurrentState = "State 2"
            
    elif CurrentState == "State 2": # New rotation Goal
        if Goal_pub == 1: # New Goal publish
            CurrentState = "State 3"
            
    elif CurrentState == "State 3": # Robot in rotation
        # Target reach or Robot stuck
        if (RobotNotMoving == 1) and (RotationOver == 0):
            CurrentState = "State 2"
        elif (RobotNotMoving == 1) and (RotationOver == 1):
            CurrentState = "State 4"

    elif CurrentState == "State 4": # New WayPoint
        if Goal_pub == 1: # New Goal publish
            CurrentState = "State 5"            
    
    elif CurrentState == "State 5": # Robot try to reach a waypoint
        if RobotNotMoving == 1: # Target reach or Robot stuck
            CurrentState = "State 4"
            
    elif CurrentState == "State 6": # Target missed
        if TargetDetect == 0:
            CurrentState = "State 2" # Rotate again 
            
            

    pub.publish(String(CurrentState))
    print(CurrentState)
    Goal_pub = 0
    RobotNotMoving = 0

    
    
if __name__ == '__main__':
    try:
        rospy.init_node('State')
        CurrentState = "State 0"
        Goal_pub = 0 #False
        Z = 0
        Stuck = 0 #False
        RobotNotMoving = 0 #False
        RobotRotation = 0 #False
        RotationOver = 0 #False
        GoalNb = -1
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback_ST0)
        rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, ImuVal)
        rospy.Subscriber("Rotation_End", String, RotEnd)
        rospy.Subscriber("tags", Tags, Target)
        rospy.spin()


    except rospy.ROSInterruptException: pass
