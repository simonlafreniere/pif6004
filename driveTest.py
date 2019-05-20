from laneSensor import findLanes
#from proximitySensor import getTraffic
from speedSensor import getSpeed
from PIL import ImageGrab
import numpy as np
import cv2
import os

from time import sleep
from pynput.keyboard import Key, Controller
import threading

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

keyboard = Controller
right_pressed = False
left_pressed = False


def right():
    global right_pressed
    right_pressed = True

    # make sure we don't fight between threads
    keyboard.release(Key.left)
    keyboard.press(Key.right)
    sleep(0.1)
    keyboard.release(Key.right)

    right_pressed = False


def left():
    global left_pressed
    left_pressed = True

    keyboard.release(Key.right)
    keyboard.press(Key.left)
    sleep(0.1)
    keyboard.release(Key.left)

    left_pressed = False


def forward():
    keyboard.release(Key.down)
    keyboard.press(Key.up)


def release():
    # on sait que c'est up, les autres sont toujours released..
    keyboard.release(Key.up)


def brake():
    # make sure we don't accelerate anymore..
    keyboard.release(Key.up)
    keyboard.press(Key.down)
    sleep(0.1)
    keyboard.release(Key.down)


while True:
    img = np.array(ImageGrab.grab(box))
    speed = getSpeed()
    lane1, lane2 = findLanes(img)
    # traffic = getTraffic(img)

    if lane1 < 0 and lane2 < 0:
        if not right_pressed:
            threading.Thread(target=right).start()
    elif lane1 > 0 and lane2 > 0:
        if not left_pressed:
            threading.Thread(target=left).start()
    else:
        if speed < 15:
            forward()
        if speed > 20:
            release()
        if speed > 25:
            threading.Thread(target=brake).start()

