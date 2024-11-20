#!/usr/bin/env python
import roslib
import rospy
import rospkg
from std_msgs.msg import String
from pynput import keyboard


class ControlNode:
    def __init__(self):
        """
        Initializes the control node, which listens to keyboard inputs and sends control commands.
        """
        # Publisher for sending control commands
        self._pub_control = rospy.Publisher("keyboard_control", String, queue_size=10)

        # Initialize movement and shooting directions
        self.movement = ""
        self.shoot_direction = ""

        # Key mappings for movement and shooting
        self.movement_keys = {
            keyboard.Key.up: "UP",
            keyboard.Key.down: "DOWN",
            keyboard.Key.left: "LEFT",
            keyboard.Key.right: "RIGHT",
        }
        self.shooting_keys = {
            "w": "W",
            "a": "A",
            "s": "S",
            "d": "D",
        }

        rospy.loginfo("Control node initialized. Use the arrow keys for movement and W, A, S, D for shooting.")

    def on_press(self, key):
        """
        Handles key press events.
        """
        try:
            # Handle movement keys
            if key in self.movement_keys:
                self.movement = self.movement_keys[key]
            
            # Handle shooting keys
            elif hasattr(key, "char") and key.char in self.shooting_keys:
                self.shoot_direction = self.shooting_keys[key.char]

            # Publish command if both movement and shooting direction are set
            if self.movement and self.shoot_direction:
                action = f"{self.movement},{self.shoot_direction}"
                self.control_pub.publish(action)
                rospy.loginfo(f"Published command: {action}")

        except Exception as e:
            rospy.logerr(f"Error in on_press: {e}")

    def on_release(self, key):
        """
        Handles key release events.
        """
        # Reset movement or shooting direction on key release
        if key in self.movement_keys:
            self.movement = None
        elif hasattr(key, "char") and key.char in self.shooting_keys:
            self.shoot_direction = None

    def start_listening(self):
        """
        Starts the keyboard listener.
        """
        # Listen to keyboard events in a separate thread
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            rospy.loginfo("Keyboard listener started.")
            rospy.spin()  # Keep the node running
            listener.join()  # Wait for the listener to stop

if __name__ == "__main__":
    try:
        # Initialize the ROS node
        rospy.init_node("control_node", anonymous=True)

        # Create an instance of the ControlNode
        node = ControlNode()

        # Start listening for keyboard inputs
        node.start_listening()

    except rospy.ROSInterruptException:
        rospy.loginfo("Control node shutting down.")