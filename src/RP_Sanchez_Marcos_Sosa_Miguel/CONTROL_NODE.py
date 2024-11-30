#!/usr/bin/python3
# -*- coding: utf-8 -*-
from pynput import keyboard
import rospy
from std_msgs.msg import String
import time

class ControlPynput:
    def __init__(self):
        self.__pub_control = rospy.Publisher("keyboard_control", String, queue_size=10)
        self.keys_state = {
            "LEFT": False,
            "RIGHT": False,
            "UP": False,
            "DOWN": False,
            "W": False,
            "A": False,
            "S": False,
            "D": False,
            "R": False,
            "Q": False,
        }
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.main()

    def on_press(self, key):
        try:
            if key == keyboard.Key.left:
                self.keys_state["LEFT"] = True
            elif key == keyboard.Key.right:
                self.keys_state["RIGHT"] = True
            elif key == keyboard.Key.up:
                self.keys_state["UP"] = True
            elif key == keyboard.Key.down:
                self.keys_state["DOWN"] = True
            elif key.char == "w":
                self.keys_state["W"] = True
            elif key.char == "a":
                self.keys_state["A"] = True
            elif key.char == "s":
                self.keys_state["S"] = True
            elif key.char == "d":
                self.keys_state["D"] = True
            elif key.char == "r":
                self.keys_state["R"] = True
            elif key.char == "q":
                self.keys_state["Q"] = True
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key == keyboard.Key.left:
                self.keys_state["LEFT"] = False
            elif key == keyboard.Key.right:
                self.keys_state["RIGHT"] = False
            elif key == keyboard.Key.up:
                self.keys_state["UP"] = False
            elif key == keyboard.Key.down:
                self.keys_state["DOWN"] = False
            elif key.char == "w":
                self.keys_state["W"] = False
            elif key.char == "a":
                self.keys_state["A"] = False
            elif key.char == "s":
                self.keys_state["S"] = False
            elif key.char == "d":
                self.keys_state["D"] = False
            elif key.char == "r":
                self.keys_state["R"] = False
            elif key.char == "q":
                self.keys_state["Q"] = False
        except AttributeError:
            pass

    def main(self):
        while not rospy.is_shutdown():
            move = ""
            shoot = ""
            decision = ""

            # Process movement
            if self.keys_state["LEFT"] and self.keys_state["UP"]:
                move = "UP_LEFT"
            elif self.keys_state["LEFT"] and self.keys_state["DOWN"]:
                move = "DOWN_LEFT"
            elif self.keys_state["RIGHT"] and self.keys_state["UP"]:
                move = "UP_RIGHT"
            elif self.keys_state["RIGHT"] and self.keys_state["DOWN"]:
                move = "DOWN_RIGHT"
            elif self.keys_state["LEFT"]:
                move = "LEFT"
            elif self.keys_state["RIGHT"]:
                move = "RIGHT"
            elif self.keys_state["UP"]:
                move = "UP"
            elif self.keys_state["DOWN"]:
                move = "DOWN"

            # Process shooting
            if self.keys_state["W"] and self.keys_state["A"]:
                shoot = "W_A"
            elif self.keys_state["W"] and self.keys_state["D"]:
                shoot = "W_D"
            elif self.keys_state["S"] and self.keys_state["A"]:
                shoot = "S_A"
            elif self.keys_state["S"] and self.keys_state["D"]:
                shoot = "S_D"
            elif self.keys_state["W"]:
                shoot = "W"
            elif self.keys_state["A"]:
                shoot = "A"
            elif self.keys_state["S"]:
                shoot = "S"
            elif self.keys_state["D"]:
                shoot = "D"

            # Process decisions
            if self.keys_state["R"]:
                decision = "R"
            elif self.keys_state["Q"]:
                rospy.loginfo("Exiting...")
                break
            elif self.keys_state["E"]:
                decision = "E"
            elif self.keys_state["N"]:
                decision = "N"
            elif self.keys_state["H"]:
                decision = "H"

            if move or shoot or decision:
                action = f"{move},{shoot},{decision}"
                rospy.loginfo(f"Publishing {action} from keyboard...")
                self.__pub_control.publish(action)

            time.sleep(0.01)


if __name__ == "__main__":
    try:
        rospy.init_node("control_node")
        rospy.loginfo("The node has started")

        ControlPynput()
    except rospy.ROSInterruptException:
        pass