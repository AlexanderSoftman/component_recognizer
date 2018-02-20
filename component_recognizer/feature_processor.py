import numpy as np
import math
import cv2
import logging

LOG = logging.getLogger(__name__)


# class should save pcb geometric size as it was
class FeatureProcessor():

    create_intermediate_images = True
    orb = None

    def __init__(self):
        # Initiate STAR detector
        self.orb = cv2.ORB_create()

    def get_features(self, image):
        # find the keypoints with ORB
        kp = self.orb.detect(
            image,
            None)

        # compute the descriptors with ORB
        kp, des = self.orb.compute(
            image,
            kp)

        if self.create_intermediate_images:
            image_with_keys = cv2.drawKeypoints(
                image,
                kp,
                None,
                color=(
                    0,
                    255,
                    0),
                flags=0)
            cv2.imwrite(
                "FeatureProcessor:get_features:1_image_with_features.png",
                image_with_keys)

        return (kp, des)

    # input:
    # two image tuples:
    # {
    #   'image': image,
    #   'kp': kp,
    #   'des' : des
    # }
    def find_matches(
            self,
            bg_image,
            bg_kp,
            bg_des,
            obj_image,
            obj_kp,
            obj_des):
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(
            bg_des,
            obj_des)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw first 10 matches.
        if self.create_intermediate_images:
            compare_img = cv2.drawMatches(
                bg_image,
                bg_kp,
                obj_image,
                obj_kp,
                matches[:10],
                None,
                flags=2)

            cv2.imwrite(
                "FeatureProcessor:get_features:2_compare_image.png",
                compare_img)
