from laneSensor import findLanes
#from proximitySensor import getTraffic
from speedSensor import getSpeed
from PIL import ImageGrab
import numpy as np
import cv2
import os

from time import sleep
from pynput.keyboard import Key, Controller

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
positionX = 400
positionY = 155

keyboard = Controller()


def right():
    keyboard.press(Key.right)
    sleep(0.07)
    keyboard.release(Key.right)


def left():
    keyboard.press(Key.left)
    sleep(0.07)
    keyboard.release(Key.left)


def forward():
    keyboard.press(Key.up)
    sleep(0.05)
    keyboard.release(Key.right)


def release():
    # on sait que c'est up, les autres sont toujours released..
    keyboard.release(Key.up)


def brake():
    keyboard.press(Key.down)
    sleep(0.05)
    keyboard.release(Key.down)


while True:
    img = np.array(ImageGrab.grab(box))
    speed = getSpeed()
    lane1, lane2 = findLanes(img)
    # traffic = getTraffic(img)

    if lane1 < 0 and lane2 < 0:
        right()
    elif lane1 > 0 and lane2 > 0:
        left()
    else:
        if speed < 10:
            forward()
        if speed > 12:
            release()
        if speed > 20:
            brake()

