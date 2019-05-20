import cv2
import numpy as np


def crop(image):
    return image[170:, :]


def get_position(image):
    img = crop(image)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)
    # convert to gray
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.threshold(blurred, 65, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=8)
    thresh = cv2.erode(thresh, None, iterations=2)
    # calculate moments of binary image
    m = cv2.moments(thresh)
    # calculate x,y coordinate of center
    c_x = int(m["m10"] / m["m00"])
    c_y = int(m["m01"] / m["m00"])

    return c_x, c_y


def main():
    print('positionSensor')


if __name__ == '__main__':
    main()
