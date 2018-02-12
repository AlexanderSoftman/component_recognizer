import numpy as np
import math
import cv2
import logging

LOG = logging.getLogger(__name__)


# class should save pcb geometric size as it was
class Warper():

    create_intermediate_images = False

    # function get img and returned warped img
    # input:
    # initial_image
    # corners of pcb
    # corners = {
    # "x_min", "x_max", "y_min", "y_max"
    # }
    def warp(
        self,
        initial_image,
            corners):

        img_size = (
            initial_image.shape[1],
            initial_image.shape[0])  # size format x, y

        src, dst = self.calc_transform_info(
            corners,
            img_size)

        # matrix of perspective transform
        M = cv2.getPerspectiveTransform(src, dst)

        # we can get inversed matrix
        # M_inv = cv2.getPerspectiveTransform(dst, src)

        warped = cv2.warpPerspective(
            initial_image,
            M,
            img_size,
            flags=cv2.INTER_LINEAR)
        if self.create_intermediate_images:
            cv2.imwrite(
                "Warper:warp:1_warped_image.png",
                warped)
        return warped

    # function
    # input:
    # 1) corners with values
    # corners["x_max"],
    # corners["y_max"],
    # corners["x_min"],
    # corners["y_min"]
    # 2) initial image size img_size
    # in format [x, y]
    # return:
    # 1) (src, dst)
    # src - points of source
    # dst - desired points
    def calc_transform_info(
        self,
        corners,
            img_size):
        polygon = [
            corners["x_max"],
            corners["y_max"],
            corners["x_min"],
            corners["y_min"]
        ]
        # LOG.critical("img_size: %s" % (img_size,))
        pcb_sides = {
            "x_side": math.sqrt(
                math.pow(corners["x_max"][0] - corners["y_min"][0], 2) +
                math.pow(corners["x_max"][1] - corners["y_min"][1], 2)),
            "y_side": math.sqrt(
                math.pow(corners["x_max"][0] - corners["y_max"][0], 2) +
                math.pow(corners["x_max"][1] - corners["y_max"][1], 2))
        }
        # LOG.critical("pcb_x_size: %s, pcb_y_size: %s" % (
            # pcb_sides["x_side"], pcb_sides["y_side"]))
        # shape koeff = pcb_x size / pcb_y size
        shape_koef = pcb_sides["x_side"] / pcb_sides["y_side"]
        # LOG.critical("shape_koef: %s" % (shape_koef,))
        # original point from image
        src = np.float32(polygon)

        # desired points
        dst = np.float32(
            [
                [img_size[0] * shape_koef, 0],  # right top dot
                [img_size[0] * shape_koef, img_size[1]],  # right down dot
                [0, img_size[1]],  # left down dot
                [0, 0]  # left top dot
            ]
        )
        # dst = np.float32(
        #     [
        #         [pcb_sides["x_side"], 0],  # right top dot
        #         [pcb_sides["x_side"], pcb_sides["y_side"]],  # right down dot
        #         [0, pcb_sides["y_side"]],  # left down dot
        #         [0, 0]  # left top dot
        #     ]
        # )
        return (src, dst)
