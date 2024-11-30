#!/usr/bin/python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import rospkg
import time

from std_msgs.msg import String, Int64
# from robotinfo_msgs.msg import User_msg
from RP_Sanchez_Marcos_Sosa_Miguel.msg import User_msg

class Infouser(object):
    def __init__(self):
        """
        Init method.
        """
        self._name = None
        self.robot = None
        self.__pub_user_info = rospy.Publisher("user_information", User_msg, queue_size=10)

        time.sleep(0.5)

        self.main()

    def main(self):
        player = User_msg()
        
        # Prompt user for information
        player.name = input("Please write your name: \n")
        player.username = input("Please write your username: \n")
        
        # Convert age input to an integer
        age_input = input("Please write your age: \n")
        
        try:
            player.age = int(age_input)  # Convert to integer
        except ValueError:
            rospy.logerr("Invalid age input. Age must be an integer.")
            return
        
        # Publish user information
        rospy.loginfo("Publishing user information...")
        self.__pub_user_info.publish(player) 

if __name__ == '__main__':
    try:
        name_node = "info_user"
        rospy.init_node(name_node)
        rospy.loginfo("The node %s has started", name_node)

        node = Infouser()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
