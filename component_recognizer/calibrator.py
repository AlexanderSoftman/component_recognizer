import numpy as np
import cv2
import glob
import json
import logging


LOG = logging.getLogger(__name__)


class Calibrator():

    calib_file_name = "camera_calibration"

    # input:
    # 1) calib_images_folder - folder with images,
    # used for creating calibration file
    # 2) black_white_intersect_x:
    # count of intersections of black and white squares in chess board
    # in x plane
    # 3) black_white_intersect_y:
    # count of intersections of black and white squares in chess board
    # in y plane
    # 4) calib_file_folder:
    # folder with result calib file
    # result:
    # function calculate calibration for camera and save
    # calibration file with name "calibration" to "calib_file_folder"
    def create_calibration(
        self,
        calib_images_folder,
        black_white_intersect_x,
        black_white_intersect_y,
            calib_file_folder):
        nx = black_white_intersect_x
        ny = black_white_intersect_y
        obj_points = []
        img_points = []
        # need points in format (0, 0, 0) - original point,
        # or (4, 2, 0). Z coordinate always zero
        objp = np.zeros((ny * nx, 3), np.float32)
        # x,y coordinates
        objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
        calib_images = glob.glob(
            calib_images_folder + "/" + "*")
        # create calibration
        for fname in calib_images:
            img = cv2.imread(fname)
            # convert to gray scale:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # find chessboard corners
            ret, corners = cv2.findChessboardCorners(
                gray,
                (nx, ny),
                None)
            if ret is True:
                # draw and display corners
                img_points.append(corners)
                obj_points.append(objp)
        # cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            obj_points,
            img_points,
            gray.shape[::-1],
            None,
            None)
        calib_struct = {
            'mtx': mtx.tolist(), 'dist': dist.tolist()}
        # add data to json struct
        with open(
            calib_file_folder + "/" + self.calib_file_name,
                'w') as calib_file:
            calib_file.write(
                json.dumps(
                    calib_struct))

    # input data:
    # 1. calib_file_folder with camera_calibration file
    # output data:
    # calib_struct = {
    #   'mtx': mtx.tolist(),
    #   'dist': dist.tolist()
    # }
    def get_calibration(
        self,
            calib_file_folder):
        with open(
            calib_file_folder + "/" + self.calib_file_name,
                'r') as calib_file:
            calib_data = calib_file.read()
            calib_struct = json.loads(calib_data)
            # restore calib file
            calib_struct['mtx'] = np.array(calib_struct['mtx'])
            calib_struct['dist'] = np.array(calib_struct['dist'])
            return calib_struct

    # input data:
    # 1) image read by cv2.imread in BGR colour scheme before calibration
    # 2) image in BGR colour scheme after calibration
    def apply_calibration(
        self,
        not_calib_image_BGR,
            calib_struct):
        return cv2.undistort(
            not_calib_image_BGR,
            calib_struct['mtx'],
            calib_struct['dist'],
            None,
            calib_struct['mtx'])
