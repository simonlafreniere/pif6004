from laneSensor import pipeline
# from proximitySensor import getTraffic
from speedSensor import get_speed
from PIL import ImageGrab
import numpy as np
import settings
import cv2
import os
from time import sleep
from pynput.keyboard import Key, Controller
import threading

import argparse

parser = argparse.ArgumentParser(description="check which user..")
parser.add_argument("-u", "--user", nargs=1)

x_pad_pat = 271
y_pad_pat = 236
width_pat = x_pad_pat + 805
height_pat = y_pad_pat + 461
x_pad_sim = 77
y_pad_sim = 166
width_sim = x_pad_sim + 917
height_sim = y_pad_sim + 546

x_pad = 0
y_pad = 0
width = 0
height = 0


keyboard = Controller()
right_pressed = False
left_pressed = False
forward_pressed = False


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
    global forward_pressed
    forward_pressed = True

    keyboard.release(Key.down)
    keyboard.press(Key.up)
    sleep(0.4)
    keyboard.release(Key.up)


def release():
    # on sait que c'est up, les autres sont toujours released..
    keyboard.release(Key.up)


def brake():
    # make sure we don't accelerate anymore..
    keyboard.release(Key.up)
    keyboard.press(Key.down)
    sleep(0.01)
    keyboard.release(Key.down)


def initialisation():
    global x_pad, y_pad, width, height
    args = parser.parse_args()
    if args.user is None or args.user[0] == 'p':
        x_pad = x_pad_pat
        y_pad = y_pad_pat
        width = width_pat
        height = height_pat
    elif args.user[0] == 's':
        x_pad = x_pad_sim
        y_pad = y_pad_sim
        width = width_sim
        height = height_sim
    global box
    box = (x_pad + 1, y_pad + 1, x_pad + width, y_pad + height)


def main():
    initialisation()
    last_speed = 0

    while True:
        img = np.array(ImageGrab.grab(box))
        speed = get_speed(last_speed)
        last_speed = speed
        lane1 = pipeline(img)
        # traffic = getTraffic(img)

        if lane1 < 0:
            if not right_pressed:
                threading.Thread(target=right).start()
        elif lane1 > 0:
            if not left_pressed:
                threading.Thread(target=left).start()
        else:
            if speed < 25:
                threading.Thread(target=forward).start()
            if speed > 30:
                release()
            if speed > 40:
                brake()
                threading.Thread(target=brake).start()


if __name__ == '__main__':
    main()
