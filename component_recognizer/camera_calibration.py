import logging
import component_recognizer.calibrator as calibrator
import cv2
import glob
import settings


black_white_intersect_x = 8
black_white_intersect_y = 6


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
    calibrator_m = calibrator.Calibrator()
    settings_m = settings.Settings()
    # create calibration_file
    calibrator_m.create_calibration(
        settings_m.calibration_images_folder,
        black_white_intersect_x,
        black_white_intersect_y,
        settings_m.calibration_file_folder)
    # get result calibration file
    camera_calibration = calibrator_m.get_calibration(
        settings_m.calibration_file_folder)
    # apply calibration to first image in calibration images folder
    calib_images = glob.glob(
        settings_m.calibration_images_folder + "/" + "*")
    for fname in calib_images:
        not_calibrated_image = cv2.imread(fname)
        cv2.imshow("not_calibrated_image", not_calibrated_image)
        while(1):
            k = cv2.waitKey(0)
            if k == ord('a'):    # a key to stop
                break
            cv2.destroyAllWindows()
        calibrated_image = calibrator_m.apply_calibration(
            not_calibrated_image,
            camera_calibration)
        cv2.imshow("calibrated_image", calibrated_image)
        while(1):
            k = cv2.waitKey(0)
            if k == ord('a'):    # a key to stop
                break
            cv2.destroyAllWindows()
        return


if __name__ == '__main__':
    main()
