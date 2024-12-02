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

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

TO RUN THE NODES:

First option, individual node execution manually:

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



Second option, running one of the launchers:

1. On a terminal write the command roslaunch RP_Sanchez_Marcos_Sosa_Miguel <launcher>. There are two launchers on the package:

- game.launch launches all functionality nodes and only the control node GAME_CONTROL.py

- pygame.launch launches the same nodes as before except that it runs the control GAME_CONTRO_PYGAME.py

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

HOW COMMUNICATION WORKS:

The nodes executed in the package perform messages communication as well as service communication. In addition, some variables that the nodes use are defined as global parameters in the launcher.

The node INFO_USER.py is the one that starts communication by publishing the data the user writes on the terminal on topic 'user_information' in 'User_msg' fromat.
Also, stores in the parameter 'user_name' the username written on the terminal.

- 'User_msg' is a type of message defined on the file user_msg.msg on folder msg. It contains two string data for name and username and int data for age.

Nodes GAME_NODE.py and RESULT_NODE.py subscribe to 'user_information' topic. GAME_NODE.py starts the game and subscribes to 'keyboard_control' topic that contains
information about the keys pressed published by one of the control nodes. Before starting the game, the user is asked to determine the difficulty of the game by calling on a terminal the service 'difficulty'. This service has datatype 'SetGameDifficulty' that is defined in the file SetGameDifficulty.srv from the folder 'srv', and consist on a string that recieves a boolean value. When game phase has started, the player color can be changed by constantly checking the value of the parameter 'change_player_color'. In addition, every time the game changes phase, the parameter 'screen' is set to contain the current phase. After the game is completed or user quits, the final score is published on topic 'result_information'. 

RESULT_NODE.py prints the user information and subscribes to 'result_information', printing the final score after completing the game. If, from a terminal, is called the service 'user_score' with the correct username, the final result of that user is retrieved. This service is 'GetUserScore' type which is defined in file GetUserScore.srv from folder 'srv'.

Control nodes, CONTROL_NODE.py and CONTROL_NODE_PYGAME.py, are used to read the keys pressed and publish information on topic 'keyboard_control'. If a number between 1 and 3 is pressed, the nodes will set the parameter 'change_player_color' that integer value for making the GAME_NODE change the player color. Both codes
share same structure, only difference is from which screen the nodes are able to read the keys.