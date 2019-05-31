from PIL import ImageGrab
import numpy as np
import cv2
import os
# import time
from pynput.keyboard import Key, Listener
import pynput.keyboard as keyboard
import threading

import argparse

parser = argparse.ArgumentParser(description="check which user..")
parser.add_argument("-u", "--user", nargs=1)

'''
All coordinates assume a screen resolution of 1366x768, and Chrome 
maximized with the Bookmarks Toolbar enabled.
pat
x_pad = 271
y_pad = 236
Play area =  x_pad+1, y_pad+1, x_pad+805, y_pad+461
'''

# Globals
# ------------------
 
x_pad_pat = 271
y_pad_pat = 236
x_pad_decal_pat = x_pad_pat + 805
y_pad_decal_pat = y_pad_pat + 461
x_pad_sim = 150
y_pad_sim = 311
x_pad_decal_sim = 1980
y_pad_decal_sim = 1338

x_pad = 0
y_pad = 0
x_pad_decal = 0
y_pad_decal = 0


def initialisation():
    global x_pad, y_pad, x_pad_decal, y_pad_decal
    x_pad = x_pad_pat
    y_pad = y_pad_pat
    x_pad_decal = x_pad_decal_pat
    y_pad_decal = y_pad_decal_pat


def on_press(key):
    # reset output
    output = [0, 0, 0, 0]

    if key == keyboard.KeyCode.from_char('q'):
        print('\ninterruption keyboard..')
        cv2.destroyAllWindows()
        exit(0)
    elif key == Key.up or key == keyboard.KeyCode.from_char('w'):
        output[1] = 1
        screen = np.array(ImageGrab.grab(box))
        lower_yellow = np.array([160, 130, 0, 255], dtype="uint16")
        upper_yellow = np.array([255, 255, 65, 255], dtype="uint16")
        yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
        screen[yellow_mask != 0] = [255, 255, 255, 255]
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 46))
    elif key == Key.down or key == Key.space or key == keyboard.KeyCode.from_char('s'):
        output[3] = 1
        screen = np.array(ImageGrab.grab(box))
        lower_yellow = np.array([160, 130, 0, 255], dtype="uint16")
        upper_yellow = np.array([255, 255, 65, 255], dtype="uint16")
        yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
        screen[yellow_mask != 0] = [255, 255, 255, 255]
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 46))
    elif key == Key.right or key == keyboard.KeyCode.from_char('d'):
        output[2] = 1
        screen = np.array(ImageGrab.grab(box))
        lower_yellow = np.array([160, 130, 0, 255], dtype="uint16")
        upper_yellow = np.array([255, 255, 65, 255], dtype="uint16")
        yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
        screen[yellow_mask != 0] = [255, 255, 255, 255]
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 46))
    elif key == Key.left or key == keyboard.KeyCode.from_char('a'):
        output[0] = 1
        screen = np.array(ImageGrab.grab(box))
        lower_yellow = np.array([160, 130, 0, 255], dtype="uint16")
        upper_yellow = np.array([255, 255, 65, 255], dtype="uint16")
        yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
        screen[yellow_mask != 0] = [255, 255, 255, 255]
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 46))

    if output != [0, 0, 0, 0]:
        training_data.append([screen, output])

        if len(training_data) % 50 == 0:
            print(len(training_data))
            np.save(file_name, training_data)


def initialisation():
    global x_pad, y_pad, x_pad_decal, y_pad_decal
    args = parser.parse_args()
    if args.user is None or args.user[0] == 'p':
        x_pad = x_pad_pat
        y_pad = y_pad_pat
        x_pad_decal = x_pad_decal_pat
        y_pad_decal = y_pad_decal_pat
    elif args.user[0] == 's':
        x_pad = x_pad_sim
        y_pad = y_pad_sim
        x_pad_decal = x_pad_decal_sim
        y_pad_decal = y_pad_decal_sim


def main():
    initialisation()

    global file_name
    file_name = 'training_data.npy'

    global training_data
    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name, allow_pickle=True))
    else:
        print('File does not exist, starting fresh!')
        training_data = []

    global box
    box = (x_pad+1, y_pad+1, x_pad_decal, y_pad_decal)

    # Collect events until released
    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()
