#!/usr/bin/python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import rospkg
import time

from std_msgs.msg import String, Int64
from RP_Sanchez_Marcos_Sosa_Miguel.msg import User_msg
from RP_Sanchez_Marcos_Sosa_Miguel.srv import GetUserScore

class Result(object):
    def __init__(self):
        """
        Init method.
        """
        # Class variables

        self.__pub_user_info = rospy.Subscriber("user_information", User_msg, self.user_info)

        self.__pub_score = rospy.Subscriber("result_information", Int64, self.results)

        self.__get_user_score = rospy.ServiceProxy('user_score', GetUserScore)

        time.sleep(2)

        self.main()

    def main (self):

        rospy.loginfo("     Subscriber")
        # Call the service and get the response

    def user_info(self, player):
        try:
            rospy.loginfo("Received user_info in callback!")
            rospy.loginfo(" The name is [%s]", player.name)
            rospy.loginfo(" The username is [%s]", player.username)
            rospy.loginfo(" The age is [%s]", player.age)
            self.name = player.name
        except Exception as e:
            rospy.logerr("Error in callback: %s", str(e))

    def results(self, score):
        try:
            rospy.loginfo("Received results in callback!")
            rospy.loginfo(" The score is [%s]", score)
            rospy.logwarn("Client service:  ")
            score_srv = self.__get_user_score.call(self.name)
            rospy.loginfo(f" The service returned:  {score_srv} for {self.name}")
        except Exception as e:
            rospy.logerr("Error in callback: %s", str(e))
        
    
if __name__ == '__main__':
    try:
        name_node = "results"
        rospy.init_node(name_node)
        rospy.loginfo("The node %s has started", name_node)

        #create and spin the node 
        node = Result()

        # Keep the node running until it is shut down
        rospy.spin()

    except rospy.ROSInterruptException:
        pass