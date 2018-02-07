import logging
import component_recognizer.settings as settings
import component_recognizer.calibrator as calibrator
import component_recognizer.contour_searcher as contour_searcher
import os
import cv2

test_image = cv2.imread(
    os.path.join(
        os.path.split(__file__)[0],
        "pcb_images",
        "pcb_1.jpg"))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
    calibrator_m = calibrator.Calibrator()
    settings_m = settings.Settings()
    contour_searcher_m = contour_searcher.ContourSearcher()
    # get calibration
    # camera_calibration = calibrator_m.get_calibration(
        # settings_m.calibration_file_folder)
    # test_image_calibrated = calibrator_m.apply_calibration(
        # test_image,
        # camera_calibration)
    test_image_calibrated = test_image
    contour_searcher_m.find_contour_dots(test_image_calibrated)


if __name__ == '__main__':
    main()
