import re
import threading

import cv2
from time import sleep
import numpy as np
from PIL import ImageGrab, Image

def getSpeed(lastSpeed):
    box = (327, 300, 328, 360)
    kernel = np.ones((5, 5), np.uint8)
    speed = 0.0
    image = np.array(ImageGrab.grab(box))
    # convert red to black
    lower_red = np.array([220, 0, 0], dtype="uint16")
    upper_red = np.array([240, 10, 50], dtype="uint16")
    red_mask = cv2.inRange(image, lower_red, upper_red)
    image[red_mask != 0] = [0, 0, 0]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (T, seg) = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY_INV)
    gauss = cv2.GaussianBlur(seg, (5, 5), 0)
    edges = cv2.Canny(gauss, 100, 200, apertureSize=3)
    dilation = cv2.dilate(edges, kernel, iterations=5)
    erosion = cv2.erode(dilation, kernel, iterations=6)
    for index, x in np.ndenumerate(erosion):
        if(x == 255):
                try:
                    index = re.sub('[(),0]', '', str(index))
                    index = float(index)
                    speed = abs((index - 44)*1.45)
                    if(abs(speed - lastSpeed) < 20):
                        return speed
                    else:
                        return lastSpeed
                except ValueError as e:
                    pass


    return speed

def main():
    print('speedSensor')


if __name__ == '__main__':
    main()