#!/usr/bin/python3
# -*- coding: utf-8 -*-
import keyboard
import rospy
from std_msgs.msg import String
import time


class ControlKeyboard:
    def __init__(self):
        self.__pub_control_keyboard = rospy.Publisher("keyboard_control", String, queue_size=10)
        self.main()

    def main(self):
        rospy.loginfo("Press 'q' to quit.")

        while not rospy.is_shutdown():
            move = ""
            shoot = ""
            decision = ""

            # Check movement keys
            if keyboard.is_pressed("left") and keyboard.is_pressed("up"):
                move = "UP_LEFT"
            elif keyboard.is_pressed("left") and keyboard.is_pressed("down"):
                move = "DOWN_LEFT"
            elif keyboard.is_pressed("right") and keyboard.is_pressed("up"):
                move = "UP_RIGHT"
            elif keyboard.is_pressed("right") and keyboard.is_pressed("down"):
                move = "DOWN_RIGHT"
            elif keyboard.is_pressed("left"):
                move = "LEFT"
            elif keyboard.is_pressed("right"):
                move = "RIGHT"
            elif keyboard.is_pressed("up"):
                move = "UP"
            elif keyboard.is_pressed("down"):
                move = "DOWN"

            # Check shooting keys (WASD)
            if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
                shoot = "W_A"
            elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
                shoot = "W_D"
            elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
                shoot = "S_A"
            elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
                shoot = "S_D"
            elif keyboard.is_pressed("w"):
                shoot = "W"
            elif keyboard.is_pressed("a"):
                shoot = "A"
            elif keyboard.is_pressed("s"):
                shoot = "S"
            elif keyboard.is_pressed("d"):
                shoot = "D"

            # Check decision keys
            if keyboard.is_pressed("r"):
                decision = "R"
            elif keyboard.is_pressed("q"):
                decision = "Q"
                rospy.loginfo("Exiting...")
                break

            # If an action is determined, publish it
            if move or shoot or decision:
                action = f"{move},{shoot},{decision}"
                rospy.loginfo(f"Publishing {action} from keyboard...")
                self.__pub_control_keyboard.publish(action)

            time.sleep(0.01)


if __name__ == "__main__":
    try:
        rospy.init_node("control_node_keyboard")
        rospy.loginfo("The node has started")

        ControlKeyboard()
    except rospy.ROSInterruptException:
        pass