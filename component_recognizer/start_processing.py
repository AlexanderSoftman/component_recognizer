import logging
import settings
import calibrator


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
    calibrator_m = calibrator.Calibrator()
    settings_m = settings.Settings()
    # get calibration file
    camera_calibration = calibrator_m.get_calibration(
        settings_m.calibration_file_folder)


if __name__ == '__main__':
    main()
