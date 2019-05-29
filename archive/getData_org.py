from PIL import ImageGrab
import numpy as np
import cv2
import os
import time
from getkeys import key_check

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
screen = None

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D,S] boolean values.
	
    '''
    output = [0,0,0,0]
    global screen
    
    if 'A' in keys:
        output[0] = 1
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))
    elif 'D' in keys:
        output[2] = 1
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))
    elif 'S' in keys:
        output[3] = 1
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))
    elif 'W' in keys:
        output[1] = 1
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))

    return screen,output


def main():

    file_name = 'training_data.npy'

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []
	
    while(True):
        keys = key_check()
        screen,output = keys_to_output(keys)
        if(output != [0,0,0,0]):
            training_data.append([screen,output])
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if len(training_data) % 100 == 0 and len(training_data) != 0:
            print(len(training_data))
            np.save(file_name,training_data)

if __name__ == '__main__':
    main()