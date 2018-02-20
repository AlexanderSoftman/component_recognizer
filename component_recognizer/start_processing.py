import logging
import os
import cv2
import numpy as np
import component_recognizer.settings as settings
import component_recognizer.calibrator as calibrator
import component_recognizer.contour_searcher as contour_searcher
import component_recognizer.warper as warper
import component_recognizer.histogram_equalizator as histogram_equalizator
import component_recognizer.feature_processor as feature_processor
import component_recognizer.pcb_component_db as pcb_component_db


pcb_image = cv2.imread(
    os.path.join(
        os.path.split(__file__)[0],
        "pcb_images",
        "pcb_pink_bg_3.jpg"))

pcb_feature_image = cv2.imread(
    os.path.join(
        os.path.split(__file__)[0],
        "pcb_images",
        "pcb_pink_bg_atmega_1.jpg"))

component_image = cv2.imread(
    os.path.join(
        os.path.split(__file__)[0],
        "components_raw_images",
        "atmega_128_1.jpg"))

pcb_pos_file = os.path.join(
    os.path.split(__file__)[0],
    "pcb_pos",
    "pcb.pos")

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
    # step 1 read pos file
    pcb_component_reader_m = pcb_component_db.PCBComponentDB(pcb_pos_file)
    return
    # initialization phase
    calibrator_m = calibrator.Calibrator()
    settings_m = settings.Settings()
    contour_searcher_m = contour_searcher.ContourSearcher(
        clean_pcb_bg)
    warper_m = warper.Warper()
    hist_equalizator_m = histogram_equalizator.HistEqualizator()
    feature_processor_m = feature_processor.FeatureProcessor()

    # get calibration
    # camera_calibration = calibrator_m.get_calibration(
        # settings_m.calibration_file_folder)
    # test_image_calibrated = calibrator_m.apply_calibration(
        # test_image,
        # camera_calibration)

    pcb_image_calibrated = pcb_image
    pcb_corners = contour_searcher_m.find_contour_dots(
        pcb_image_calibrated)
    warped_pcb_image = warper_m.warp(
        pcb_image_calibrated,
        pcb_corners)
    pcb_image_res = hist_equalizator_m.equalizate(
        warped_pcb_image)


    component_image_res = component_image
    # component_corners = contour_searcher_m.find_contour_dots(
    #     component_image_calibrated)
    # warped_component_image = warper_m.warp(
    #     component_image_calibrated,
    #     component_corners)
    # component_image_equalizated = hist_equalizator_m.equalizate(
    #     warped_component_image)

    bg_kp, bg_des = feature_processor_m.get_features(pcb_feature_image)
    obj_kp, obj_des = feature_processor_m.get_features(component_image_res)
    feature_processor_m.find_matches(
        pcb_feature_image,
        bg_kp,
        bg_des,
        component_image_res,
        obj_kp,
        obj_des)


if __name__ == '__main__':
    main()
