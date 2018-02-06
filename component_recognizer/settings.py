import os


class Settings():
    # path to caliration file
    calibration_file_folder = os.path.join(
        os.path.split(__file__)[0],
        "calibration")

    # path to calibration
    calibration_images_folder = os.path.join(
        os.path.split(__file__)[0],
        "calib_images")
