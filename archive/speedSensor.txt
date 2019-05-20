import re
import cv2
from time import sleep
import numpy as np
from PIL import ImageGrab, Image
from directkeys import PressKey, ReleaseKey, W, A, S, D, X

def straight():
    PressKey(W)
    sleep(0.2)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)

def release():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
	
def brake():
    PressKey(X)
    sleep(0.1)
    ReleaseKey(X)
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def screenGrab():
    box = (327,300,328,360)
    kernel = np.ones((5,5), np.uint8)
    bad_chars = '()0'
    lastSpeed = 0.0
    while(True):
        image =  np.array(ImageGrab.grab(box))
        # convert red to black
        lower_red = np.array([220,0,0], dtype = "uint16")
        upper_red = np.array([240,10,50], dtype = "uint16")
        red_mask = cv2.inRange(image, lower_red, upper_red)
        image[red_mask != 0] = [0,0,0]
        #image = cv2.resize(image, (120,200))
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        (T, seg) = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY_INV)
        gauss = cv2.GaussianBlur(seg,(5,5),0)
        edges = cv2.Canny(gauss,100,200,apertureSize = 3)
        dilation = cv2.dilate(edges, kernel, iterations=5)
        erosion = cv2.erode(dilation, kernel, iterations=6)
        for index, x in np.ndenumerate(erosion):
            if(x == 255):
                try:
                    index = re.sub('[(),0]', '', str(index))
                    index = float(index)
                    speed = abs((index - 44)*1.45)
                    if(abs(speed - lastSpeed) < 20):
                        lastSpeed = speed
                        print(speed)
                    else:
                        print(lastSpeed)
                except ValueError as e:
                    print(lastSpeed)

        if(speed<35 and lastSpeed<35):
            straight()
        if(speed>40 and lastSpeed>40):
            release()
        if(speed>55 and lastSpeed>55):
            brake()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()