import numpy as np
import cv2


class Warper():

    create_intermediate_images = True

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

        polygon = [
            corners["x_max"],
            corners["y_max"],
            corners["x_min"],
            corners["y_min"]
        ]

        img_size = (
            initial_image.shape[1],
            initial_image.shape[0])  # size format x, y

        # original point from image
        src = np.float32(polygon)

        # desired points
        dst = np.float32(
            [
                [img_size[0], 0],  # right top dot
                [img_size[0], img_size[1]],  # right down dot
                [0, img_size[1]],  # left down dot
                [0, 0]  # left top dot
            ]
        )

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
