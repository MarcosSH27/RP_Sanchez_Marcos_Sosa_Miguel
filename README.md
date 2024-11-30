# RP_Sanchez_Marcos_Sosa_Miguel

To run all the nodes included in this repository, it is necessary to install python and the next libraries:

- roslib
- rospy
- rospkg
- time
- random
- sys
- os
- pygame
- math
- pynput


TO RUN THE NODES:

1. Run roscore command to enable master communication between nodes in ROS.

2. Run in a new terminal the node INFO_USER.py (all nodes are included in this repository).

- On the terminal, the user will be asked their name, username and age. Wait until all nodes are running before giving the data.

3. In another terminal, go to directory .../RP_Sanchez_Marcos_Sosa_Miguel/nodes and run the node GAME_NODE.py. 
It is important that the GAME_NODE.py node is runned from that directory in order to be able to access to the additional files
contained on folder nodes the file uses during execution.

- After running it, a blank screen will be displayed. Nothing will be displayed until the user information is recieved from INFO_USER.py

4. In a new terminal, run only one of the control nodes. It could be CONTROL_NODE.py or CONTROL_NODE_PYGAME.py.
Running both nodes at the same time would cause undesired game responses.

- CONTROL_NODE.py: for being able to read keyboard inputs, click on the game screen created after running GAME_NODE.py
- CONTROL_NODE_PYGAME.py: a new little screen is created. To read keyboard inputs, click on this new little screen.

5. Run in a different terminal the node RESULT_NODE.py.

- This node will first recieve and print the user information after INFO_USER.py sends it, and then print the final score when recieved from GAME_NODE.py


HOW COMMUNICATION WORKS:

The node INFO_USER.py is the one that starts communication by publishing the data the user writes on the terminal on topic 'user_information' in 'User_msg' fromat.

- 'User_msg' is a type of message defined on the file user_msg.msg on folder msg. It contains two string data for name and username and int data for age.

Nodes GAME_NODE.py and RESULT_NODE.py subscribe to 'user_information' topic. GAME_NODE.py starts the game and subscribes to 'keyboard_control' topic that contains
information about the keys pressed published by one of the control nodes. After the game is completed or user quits, the final score is published on topic 'result_information'. RESULT_NODE.py prints the user information and subscribes to 'result_information', printing the final score after completing the game.

Control nodes, CONTROL_NODE.py and CONTROL_NODE_PYGAME.py, are used to read the keys pressed and publish information on topic 'keyboard_control'. Both codes
share same structure, only difference is from which screen the nodes are able to read the keys.