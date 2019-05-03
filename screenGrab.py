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
    vertices = np.array([[0,460],[0,230],[300,150],[475,150],[800,230],[800,460]], np.int32)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,      20,         15)
    draw_lines(processed_img,lines)
    return processed_img

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)
		
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