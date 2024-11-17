#!/usr/bin/python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import rospkg
import time

from std_msgs.msg import String, Int64
from robotinfo_msgs.msg import User


class RobotInfoSub(object):
    def __init__(self):
        """
        Init method.
        """
        # Class variables

        self.__pub_user_info = rospy.Subscriber("user_information", User, self.callback1)

        time.sleep(3)

        self.main()

    def main (self):

        rospy.loginfo("     Subscriber")

    def callback1(self, data1):

        rospy.loginfo(" Hello I'm the callback 1 subscriber..." )
        rospy.loginfo(" The name is [%s]", data1)

    def callback2(self, data2):
        print(data2)
        
        rospy.loginfo(" Hello I'm the callback 2 subscriber..." )
        rospy.loginfo(" The username is [%s]", str(data2))
    
    def callback3(self,data3):
        print(data3)
        rospy.loginfo(" Hello I'm the callback 3 subscriber..." )
        rospy.loginfo(" The age is [%s]", str(data3))


if __name__ == '__main__':
    try:
        # Initialize the node with a name, e.g., 'name_robot'
        rospy.init_node('robotinfosub')

        # Log an informational message
        rospy.loginfo("The node robot_info has started")

        #create and spin the node 
        node = RobotInfoSub()

        # Keep the node running until it is shut down
        rospy.spin()

    except rospy.ROSInterruptException:
        pass