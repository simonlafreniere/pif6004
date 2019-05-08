import numpy as np
from PIL import ImageGrab
import pytesseract
import os
import cv2
from time import sleep
from directkeys import PressKey, ReleaseKey, W, A, S, D, X

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
    while(True):
        screen =  np.array(ImageGrab.grab(box))
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        (T, screen) = cv2.threshold(screenGray, 230, 255, cv2.THRESH_BINARY_INV)
        screen = cv2.resize(screen, (80,46))
        cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        str = pytesseract.image_to_string(screen, lang = 'eng')
        if(str.isdigit()):
            speed = int(str)
            print(str)
            if(speed<20):
                straight()
            if(speed>30):
                release()
            if(speed>40):
                brake()
				
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()