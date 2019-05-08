import numpy as np
from PIL import ImageGrab
import pytesseract
import os
import cv2
from time import sleep
from directkeys import PressKey, ReleaseKey, W, A, S, D, X
import scipy.misc

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
kernel = np.ones((5,5),np.uint8)

def straight():
    PressKey(W)
    sleep(2)
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
    sleep(0.5)
    ReleaseKey(X)
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def screenGrab():
    box = (338,351,365,363)
    i = 1
    while(True):
        screen =  np.array(ImageGrab.grab(box))
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        (T, screen) = cv2.threshold(screenGray, 230, 255, cv2.THRESH_BINARY_INV)
        screen = cv2.resize(screen, (80,46))
        cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        scipy.misc.imsave('speed_data/outfile' + str(i) + '.jpg', screen)
        i += 1
        im2str = pytesseract.image_to_string(screen, lang = 'eng')
        if(im2str.isdigit()):
            speed = int(im2str)
            print(im2str)
            if(speed<30):
                straight()
            if(speed>40):
                release()
            if(speed>50):
                brake()
				
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()