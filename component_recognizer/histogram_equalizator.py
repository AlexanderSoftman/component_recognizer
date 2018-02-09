import cv2
import logging

LOG = logging.getLogger(__name__)


class HistEqualizator():

    create_intermediate_images = False

    # input:
    # image
    # output:
    # image with equlizated histogram
    def equalizate(
        self,
            image):
        # create a CLAHE object (Arguments are optional).
        if self.create_intermediate_images:
            cv2.imwrite(
                "HistEqualizator:equalizate:0_image_original.png",
                image)
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

        # bad method:
        # # equalize the histogram of the Y channel
        # image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
        # # convert the YUV image back to RGB format
        # image_equalizated = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        # new method
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8))
        image_yuv[:, :, 0] = clahe.apply(image_yuv[:, :, 0])
        image_equalizated = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)
        if self.create_intermediate_images:
            cv2.imwrite(
                "HistEqualizator:equalizate:1_image_equalizated.png",
                image_equalizated)
        return image_equalizated
