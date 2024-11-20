#!/usr/bin/python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import rospkg
import time
import random
import sys
import os
import pygame
import math

from std_msgs.msg import String

# Initialize pygame
pygame.init()

class Control_Pygame(object):
    def __init__(self):
        """
        Init method.
        """
        pygame.display.set_mode((200, 100))  # Create a small dummy window

        self.__pub_control_pygame = rospy.Publisher("keyboard_control", String, queue_size=10)

        self.main()

    def main(self):
        
        # Initialize state of keys
        keys_state = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_w: False,   # W key for up
            pygame.K_a: False,   # A key for left
            pygame.K_s: False,   # S key for down
            pygame.K_d: False    # D key for right
        }

        while not rospy.is_shutdown():
            pygame.event.pump()  # Update the event queue
            
            move = ""
            shoot = ""
            
            # Loop through all events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        keys_state[pygame.K_LEFT] = True
                    elif event.key == pygame.K_RIGHT:
                        keys_state[pygame.K_RIGHT] = True
                    elif event.key == pygame.K_UP:
                        keys_state[pygame.K_UP] = True
                    elif event.key == pygame.K_DOWN:
                        keys_state[pygame.K_DOWN] = True
                    elif event.key == pygame.K_w:
                        keys_state[pygame.K_w] = True
                    elif event.key == pygame.K_a:
                        keys_state[pygame.K_a] = True
                    elif event.key == pygame.K_s:
                        keys_state[pygame.K_s] = True
                    elif event.key == pygame.K_d:
                        keys_state[pygame.K_d] = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys_state[pygame.K_LEFT] = False
                    elif event.key == pygame.K_RIGHT:
                        keys_state[pygame.K_RIGHT] = False
                    elif event.key == pygame.K_UP:
                        keys_state[pygame.K_UP] = False
                    elif event.key == pygame.K_DOWN:
                        keys_state[pygame.K_DOWN] = False
                    elif event.key == pygame.K_w:
                        keys_state[pygame.K_w] = False
                    elif event.key == pygame.K_a:
                        keys_state[pygame.K_a] = False
                    elif event.key == pygame.K_s:
                        keys_state[pygame.K_s] = False
                    elif event.key == pygame.K_d:
                        keys_state[pygame.K_d] = False

            # Check for diagonal movement combinations
            if keys_state[pygame.K_LEFT] and keys_state[pygame.K_UP]:
                move = "UP_LEFT"
            elif keys_state[pygame.K_LEFT] and keys_state[pygame.K_DOWN]:
                move = "DOWN_LEFT"
            elif keys_state[pygame.K_RIGHT] and keys_state[pygame.K_UP]:
                move = "UP_RIGHT"
            elif keys_state[pygame.K_RIGHT] and keys_state[pygame.K_DOWN]:
                move = "DOWN_RIGHT"
            # Check for individual movement
            elif keys_state[pygame.K_LEFT]:
                move = "LEFT"
            elif keys_state[pygame.K_RIGHT]:
                move = "RIGHT"
            elif keys_state[pygame.K_UP]:
                move = "UP"
            elif keys_state[pygame.K_DOWN]:
                move = "DOWN"

            # Check for WASD combinations
            if keys_state[pygame.K_w] and keys_state[pygame.K_a]:
                shoot = "W_A"
            elif keys_state[pygame.K_w] and keys_state[pygame.K_d]:
                shoot = "W_D"
            elif keys_state[pygame.K_s] and keys_state[pygame.K_a]:
                shoot = "S_A"
            elif keys_state[pygame.K_s] and keys_state[pygame.K_d]:
                shoot = "S_D"
            elif keys_state[pygame.K_w]:
                shoot = "W"
            elif keys_state[pygame.K_a]:
                shoot = "A"
            elif keys_state[pygame.K_s]:
                shoot = "S"
            elif keys_state[pygame.K_d]:
                shoot = "D"
            # If an action is determined, publish it
            if move or shoot:
                action = f"{move},{shoot}"
                rospy.loginfo(f"Publishing {action} from keyboard...")
                self.__pub_control_pygame.publish(action)   

            time.sleep(0.01)


if __name__ == '__main__':
    try:
        name_node = "control_node_pygame"
        rospy.init_node(name_node)
        rospy.loginfo("The node %s has started", name_node)

        node = Control_Pygame()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
