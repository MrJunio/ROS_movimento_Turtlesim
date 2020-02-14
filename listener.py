#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose

def callback(msg):
    print('posicao em x:', msg.x)
    print('posicao em y:', msg.y)

rospy.init_node('listener')
rospy.Subscriber('turtle1/pose', Pose, callback)
rospy.spin()