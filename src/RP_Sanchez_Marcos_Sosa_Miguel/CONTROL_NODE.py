#!/usr/bin/python3
# -*- coding: utf-8 -*-
import roslib
from std_msgs.msg import String
import rospy
import curses
from std_msgs.msg import String

class GameControlNode:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('game_control_node')

        # Publisher to send control commands to the game
        self.__pub_control = rospy.Publisher('keyboard_control', String, queue_size=10)

        # Initialize the control state
        self.running = True

    def get_control_message(self, key):
        """Converts key press into a movement and shooting direction."""
        movement = ""
        shoot_direction = ""

        if key == ord('q'):  # Quit
            self.running = False
        elif key == curses.KEY_LEFT:
            movement = 'LEFT'
        elif key == curses.KEY_RIGHT:
            movement = 'RIGHT'
        elif key == curses.KEY_UP:
            movement = 'UP'
        elif key == curses.KEY_DOWN:
            movement = 'DOWN'
        elif key == ord('j'):
            movement = 'DOWN_LEFT'
        elif key == ord('l'):
            movement = 'DOWN_RIGHT'
        elif key == ord('u'):
            movement = 'UP_LEFT'
        elif key == ord('o'):
            movement = 'UP_RIGHT'
        elif key == ord('w'):  # Shoot Up
            shoot_direction = 'W'
        elif key == ord('s'):  # Shoot Down
            shoot_direction = 'S'
        elif key == ord('a'):  # Shoot Left
            shoot_direction = 'A'
        elif key == ord('d'):  # Shoot Right
            shoot_direction = 'D'

        # Return combined action string for movement and shooting
        return f"{movement},{shoot_direction}"

    def run(self, stdscr):
        # Set up curses window
        curses.curs_set(0)  # Hide the cursor
        stdscr.nodelay(1)   # Non-blocking input
        stdscr.timeout(100)  # Set the screen refresh timeout

        while self.running:
            key = stdscr.getch()  # Get user input

            if key == -1:
                continue  # No key pressed, continue looping

            # Convert key press into control message
            control_msg = self.get_control_message(key)

            # If there is any control message to publish
            if control_msg:
                self.__pub_control.publish(control_msg)

            # Check if 'q' is pressed to quit the program
            if key == ord('q'):
                self.running = False

        curses.endwin()  # End curses mode

if __name__ == '__main__':
    try:
        # Create GameControlNode instance and run the control loop
        node = GameControlNode()
        
        # Start curses and run the game control loop
        curses.wrapper(node.run)

        # Keep the node running until it is shut down
        rospy.spin()

    except rospy.ROSInterruptException:
        pass