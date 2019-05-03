from PIL import ImageGrab
import numpy as np
import cv2
import os
import time

"""
All coordinates assume a screen resolution of 1366x768, and Chrome 
maximized with the Bookmarks Toolbar enabled.

x_pad = 271
y_pad = 236
Play area =  x_pad+1, y_pad+1, x_pad+805, y_pad+461
"""

# Globals
# ------------------
 
x_pad = 271
y_pad = 236

def process_img(image):
    # convert yellow lines to white lines
    lower_yellow = np.array([160,130,0], dtype = "uint16")
    upper_yellow = np.array([255,255,65], dtype = "uint16")
    yellow_mask = cv2.inRange(image, lower_yellow, upper_yellow)
    image[yellow_mask != 0] = [255,255,255]
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2= 300)
    return processed_img

def screenGrab(): 
    last_time = time.time()
    box = (x_pad+1, y_pad+1, x_pad+805, y_pad+461)
    while(True):
        screen =  np.array(ImageGrab.grab(box))
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        #cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()