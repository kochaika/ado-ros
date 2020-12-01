#!/usr/bin/env python3
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import Twist2DStamped
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from solution.solution import LfChallengeTaskSolution
import numpy as np
import cv2

class MyNode(DTROS):

    def __init__(self, node_name):
        super(MyNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        self.bridge = CvBridge()
        self.solution = LfChallengeTaskSolution({'env': self})
        self.cur_img = None
        self.pub = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)
        self.sub_image = rospy.Subscriber(
            "~image/compressed",
            CompressedImage,
            self.image_cb,
            buff_size=10000000,
            queue_size=1
        )
        rospy.sleep(1)
        self.solution.solve()


    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(0.5) # 1Hz
        while not rospy.is_shutdown():
            rate.sleep()

    def image_cb(self, image_msg):
        try:
            image = self.bridge.compressed_imgmsg_to_cv2(image_msg)
            self.cur_img = image
        except ValueError as e:
            self.logerr('Could not decode image: %s' % e)
            return
        print(image.shape)

    def step(self, vels):
        msg = Twist2DStamped()
        msg.v = vels[0]
        msg.omega = vels[1]
        rospy.loginfo("Publishing speeds:  {} {} ".format(msg.v, msg.omega))
        self.pub.publish(msg)
        return (self.cur_img, None, None, None)

    def render(self):
        pass

if __name__ == '__main__':
    # create the node
    node = MyNode(node_name='circle_drive_node')
    # run node
    #node.run()
    # keep spinning
    #rospy.spin()
