from laneSensor import findLanes
# from proximitySensor import getTraffic
from speedSensor import getSpeed
from PIL import ImageGrab
import numpy as np
import settings
import cv2
import os
from time import sleep
from pynput.keyboard import Key, Controller
import threading

x_pad = settings.x_pad
y_pad = settings.y_pad
width = settings.width
height = settings.height
box = (x_pad + 1, y_pad + 1, x_pad + width, y_pad + height)
keyboard = Controller()
right_pressed = False
left_pressed = False
forward_pressed = False
brake_pressed = False

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
    global brake_pressed
    brake_pressed = True
    # make sure we don't accelerate anymore..
    keyboard.release(Key.up)
    keyboard.press(Key.down)
    sleep(0.2)
    keyboard.release(Key.down)


def main():
    last_speed = 0

    while True:
        img = np.array(ImageGrab.grab(box))
        speed = getSpeed(last_speed)
        last_speed = speed
        lane1, lane2 = findLanes(img)
        # traffic = getTraffic(img)

        if lane1 < 0 and lane2 < 0:
            if not right_pressed:
                threading.Thread(target=right).start()
        elif lane1 > 0 and lane2 > 0:
            if not left_pressed:
                threading.Thread(target=left).start()
        else:
            if speed < 25:
                threading.Thread(target=forward).start()
            if speed > 30:
                release()
            if speed > 40:
                threading.Thread(target=brake).start()


if __name__ == '__main__':
    main()
