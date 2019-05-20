from laneSensor import findLanes
from positionSensor import getPosition
#from proximitySensor import getTraffic
from speedSensor import getSpeed
from PIL import ImageGrab
import numpy as np
import cv2
import os

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
box = (x_pad+1, y_pad+1, x_pad+805, y_pad+461)

while(True):
    img = np.array(ImageGrab.grab(box))
    speed = getSpeed()
    position = getPosition(img)
    lane1,lane2 = findLanes(img)
	#traffic = getTraffic(img)
    print(speed, position, lane1, lane2)
