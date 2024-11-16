#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

from RP_Sanchez_Marcos_Sosa_Miguel.src.RP_Sanchez_Marcos_Sosa_Miguel.info_user import Infouser

if __name__ == '__main__':
    try:
        name_node = "info_user"

        rospy.init_node(name_node)
        rospy.loginfo("Node %s has started", name_node)

        node = Infouser()

        rospy.spin()

    except rospy.ROSInterruptException:
        pass
