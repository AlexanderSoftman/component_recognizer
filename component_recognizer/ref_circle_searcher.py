import cv2
import numpy as np


class RefCircleSearcher():

    def find_ref_circles(self, image_path):
        print(image_path)
        img = cv2.imread(image_path)
        img = cv2.medianBlur(img,5)
        print(img.shape)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,20,
                                    param1=50,param2=30,minRadius=0,maxRadius=0)

        circles = np.uint16(np.around(circles))
        print(circles)
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        cv2.imwrite(
            "RefCircleSearcher:res_image.png",
            img)
