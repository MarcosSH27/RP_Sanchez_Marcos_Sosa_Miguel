#!/usr/bin/python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import rospkg
import time

from std_msgs.msg import String, Int64
from robotinfo_msgs.msg import Robotinfomsg

class Infouser(object):
    def __init__(self):
        """
        Init method.
        """
        self._name = None
        self.robot = None
        self.__pub_user_info = rospy.Publisher("user_information", Robotinfomsg, queue_size=10)

        time.sleep(3)

        self.main()

    def main (self):
        
        player = Robotinfomsg()
        player.name = input("Please write your name: \n")
        player.surname = input("Please write your surname: \n")
        player.age = input("Please write your age: \n")

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