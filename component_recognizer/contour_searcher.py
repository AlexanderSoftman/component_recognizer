import cv2
import numpy as np
import logging

LOG = logging.getLogger(__name__)


class ContourSearcher():

    create_intermediate_images = False

    harris_corners = {
        'neighbourhood_block_size': 2,
        'sobel_derivative_aperture': 3,
        'free_parameter': 0.04
    }

    def __init__(
        self,
        clean_pcb_bg,
            delta_sensitivity=20):
        self.pcb_mask = {
            'hsv_min': np.array([
                clean_pcb_bg[0] - delta_sensitivity,
                50,
                50]),
            'hsv_max': np.array([
                clean_pcb_bg[0] + delta_sensitivity,
                255,
                255])
        }

    # function find only background of the image
    # input: RGB image read by cv2.imread
    # output: mask
    def find_bg_only(
        self,
            image):
        # find pink mask:
        # apply colour filtering
        hsv_image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2HSV)

        # create mask
        mask = cv2.inRange(
            hsv_image,
            self.pcb_mask['hsv_min'],
            self.pcb_mask['hsv_max'])

        if self.create_intermediate_images:
            cv2.imwrite(
                "ContourSearcher:find_contour_dots:2_bg_mask.png",
                mask)
        # morphological opening to background mask
        kernel = np.ones((15, 15), np.uint8)
        bg_mask_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        if self.create_intermediate_images:
            cv2.imwrite(
                "ContourSearcher:find_contour_dots:3_bg_mask_opening.png",
                bg_mask_opening)
        return bg_mask_opening

    # function find all corners of image
    # input:
    # white background and black all other
    # output array of corners res_corners
    # res_corners[:, 3] - x?
    # res_corners[:, 2] - y?

    def find_corners(self, bg_mask):
        # Shi-Tomashi test algorithm
        # maximum_corners = 6
        # quality_level = 0.01
        # minimum_distance = 500
        #
        # corners = cv2.goodFeaturesToTrack(
        #     bg_mask,
        #     maximum_corners,
        #     quality_level,
        #     minimum_distance)
        # corners = np.int0(corners)
        # LOG.critical("count of corners: %s, corners: %s" % (
        #    len(corners), corners))
        # for i in corners:
        #     x, y = i.ravel()
        #     cv2.circle(
        #         self.image_m,
        #         (x, y),
        #         3,
        #         255,
        #         -1)
        # if self.create_intermediate_images:
        #     cv2.imwrite(
        #         "ContourSearcher:find_contour_dots:-1_testing_Shi-Tomashi algorithm.png",
        #         self.image_m)

        # find Harris corners
        bg_mask = np.float32(bg_mask)
        dst = cv2.cornerHarris(
            bg_mask,
            self.harris_corners['neighbourhood_block_size'],
            self.harris_corners['sobel_derivative_aperture'],
            self.harris_corners['free_parameter'])
        dst = cv2.dilate(
            dst,
            None)
        ret, dst = cv2.threshold(
            dst,
            0.01 * dst.max(),
            255,
            0)
        dst = np.uint8(dst)

        # find centroids
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(
            dst)

        # define the criteria to stop and refine the corners
        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            100,
            0.001)
        corners = cv2.cornerSubPix(
            bg_mask,
            np.float32(centroids),
            (5, 5),
            (-1, -1),
            criteria)

        # Now draw them
        res = np.hstack((centroids, corners))
        res = np.int0(res)
        # original_image[
        #     res[:, 1],
        #     res[:, 0]] = [0, 0, 255]
        # original_image[
        #     res[:, 3],
        #     res[:, 2]] = [0, 255, 0]
        # cv2.imwrite('subpixel5.png', original_image)
        return res

    # function find 4 corners with maximum x, minimum x,
    # maximum y, minimum y
    # input:
    # corners list
    # output dict of 4 corners
    # corners = {
    # "x_min", "x_max", "y_min", "y_max"
    # }
    def filter_corners(self, all_corners):
        corners = {
            "x_min": None,
            "x_max": None,
            "y_min": None,
            "y_max": None
        }
        all_corners = sorted(
            all_corners,
            key=lambda value: value[3])
        corners["y_min"] = (all_corners[0][2], all_corners[0][3])
        corners["y_max"] = (all_corners[-1][2], all_corners[-1][3])
        all_corners = sorted(
            all_corners,
            key=lambda value: value[2])
        corners["x_min"] = (all_corners[0][2], all_corners[0][3])
        corners["x_max"] = (all_corners[-1][2], all_corners[-1][3])
        # LOG.critical("old method corners: %s" % (corners,))
        return corners

    # "x_min"
    # input:
    # original image after apply camera calibration
    # output:
    # array of dots for image contour
    def find_contour_dots(
        self,
            image):
        # test only
        self.image_m = image.copy()
        if self.create_intermediate_images:
            cv2.imwrite(
                "ContourSearcher:find_contour_dots:1_original_image.png",
                image)
        bg_mask = self.find_bg_only(image)
        res_corners = self.find_corners(bg_mask)
        # LOG.debug("res_corners: %s" % (res_corners,))
        pcb_corners = self.filter_corners(res_corners)
        # LOG.debug("pcb_corners: %s" % (pcb_corners,))
        image_with_corners = image.copy()
        image_with_corners[
            pcb_corners["x_min"][1],
            pcb_corners["x_min"][0]] = [255, 255, 255]
        image_with_corners[
            pcb_corners["x_max"][1],
            pcb_corners["x_max"][0]] = [255, 255, 255]
        image_with_corners[
            pcb_corners["y_min"][1],
            pcb_corners["y_min"][0]] = [255, 255, 255]
        image_with_corners[
            pcb_corners["y_max"][1],
            pcb_corners["y_max"][0]] = [255, 255, 255]
        if self.create_intermediate_images:
            cv2.imwrite(
                "ContourSearcher:find_contour_dots:4_image_with_corners.png",
                image_with_corners)
        return pcb_corners
