import logging
import os
import cv2
import numpy as np
import component_recognizer.settings as settings
import component_recognizer.calibrator as calibrator
import component_recognizer.contour_searcher as contour_searcher
import component_recognizer.warper as warper


test_image = cv2.imread(
    os.path.join(
        os.path.split(__file__)[0],
        "pcb_images",
        "pcb_pink_bg_3.jpg"))

# this color used for filtering pcb image by color
delta_sensitivity = 20
# hsv pink: [136 105 255]
clean_pcb_bg = np.array([
    136,
    105,
    255])


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
    calibrator_m = calibrator.Calibrator()
    settings_m = settings.Settings()
    contour_searcher_m = contour_searcher.ContourSearcher(
        clean_pcb_bg)
    warper_m = warper.Warper()
    # get calibration
    # camera_calibration = calibrator_m.get_calibration(
        # settings_m.calibration_file_folder)
    # test_image_calibrated = calibrator_m.apply_calibration(
        # test_image,
        # camera_calibration)
    test_image_calibrated = test_image
    pcb_corners = contour_searcher_m.find_contour_dots(
        test_image_calibrated)
    warped_image = warper_m.warp(
        test_image_calibrated,
        pcb_corners)


if __name__ == '__main__':
    main()
