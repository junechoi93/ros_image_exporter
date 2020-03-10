#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""

import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_exporter:
	
    def __init__(self):
        parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
        parser.add_argument("bag_file", help="Input ROS bag.")
        parser.add_argument("export_dir", help="Output directory.")
        parser.add_argument("image_topic", help="Image topic.")
        parser.add_argument("-f", "--force", action="store_true", help="overwrite old data")

        args = parser.parse_args()

        # input/output paths
        self.bag_file = args.bag_file
        self.export_path = args.export_dir

        if os.path.exists(self.export_path) and not args.force:
            raise UserWarning("path "+self.export_path+" already exists!")

        # image topic
        self.image_topic = args.image_topic

        # instantiate CvBridge
        self.bridge = CvBridge()

    def export(self):
        print("Extract images from %s on topic %s into %s" % (self.bag_file,
                                                              self.image_topic, self.export_path))

        # create export dir
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

        bag = rosbag.Bag(self.bag_file, "r")
        count = 0
        for topic, msg, t in bag.read_messages(topics=[self.image_topic]):
            try:
                cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            except CvBridgeError, e:
                print(e)
            else:
                cv2.imwrite(os.path.join(self.export_path, "frame%06i.png" % count), cv_img)
                print("Wrote image %i" % count)

                count += 1

        bag.close()


if __name__ == '__main__':
    image_exporter().export()
