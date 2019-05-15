from PIL import ImageGrab
import numpy as np
import cv2
import os
# import time
from pynput.keyboard import Key, Listener

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
x_pad_sim = 230
y_pad_sim = 350
x_pad_decal_sim = x_pad_sim + 1676
y_pad_decal_sim = y_pad_sim + 912

x_pad = 0
y_pad = 0
x_pad_decal = 0
y_pad_decal = 0

output = [0, 0, 0, 0]


def initialisation():
    global x_pad, y_pad, x_pad_decal, y_pad_decal
    x_pad = x_pad_pat
    y_pad = y_pad_pat
    x_pad_decal = x_pad_decal_pat
    y_pad_decal = y_pad_decal_pat


def on_press(key):
    global output

    if key == 'q':
        global quit_now
        quit_now = True
    elif key == Key.up:
        output[1] = 1
    elif key == Key.down or key == Key.space:
        output[3] = 1
    elif key == Key.right:
        output[0] = 1
    elif key == Key.left:
        output[3] = 1


def main():
    global output

    # Collect events until released
    with Listener(on_press=on_press) as listener:
        listener.join()

    file_name = 'training_data.npy'

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []

    box = (x_pad+1, y_pad+1, x_pad_decal, y_pad_decal)

    while True:
        screen = np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 46))
        training_data.append([screen, output])
        # reset output
        output = [0, 0, 0, 0]
        
        if quit_now:
            cv2.destroyAllWindows()
            break

        if len(training_data) % 500 == 0:
            print(len(training_data))
            np.save(file_name, training_data)


if __name__ == '__main__':
    main()
