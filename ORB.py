'''
как я себе это представляю - есть некий алгоритм, который знает,
что такое реперная точка и может на изображении все реперные точки.
Пропускаем изображение через этот алгоритм - находим все точки

Далее для конкретной платы у нас поступает информация -
какое должно быть рассточние между этими точками

сравниваем расстояние с фотки с расстоянием из поступивших данных ->
можем поворачивать изображение
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('images/plata_good.jpg', 0)

# Initiate STAR detector
orb = cv2.ORB()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(
    img,
    kp,
    color=(0, 255, 0),
    flags=0)
plt.imshow(img2)
plt.show()
