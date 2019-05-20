import numpy as np
from PIL import ImageGrab
import cv2
from time import sleep
from directkeys import PressKey,ReleaseKey, W, A, S, D
from alexnet import alexnet

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
WIDTH = 80
HEIGHT = 46
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'MODERN-CAR-RACING-{}-{}-{}-epochs.model'.format(LR, 'alexnet',EPOCHS)
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def straight():
    PressKey(W)
    sleep(2)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)

def release():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
	
def brake():
    PressKey(X)
    sleep(0.1)
    ReleaseKey(X)
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def main():

    box = (x_pad+1, y_pad+1, x_pad+805, y_pad+461)
    i = 0
    while(True):
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))
        #cv2.imshow('',screen)
        moves = list(np.around(model.predict([screen.reshape(80,46,1)])[0]))
		
        if moves == [1,0,0,0]:
            print(f'left  {i}:')
            left()
            print(moves)
        elif moves == [0,1,0,0]:
            print(f'straight  {i}:')
            straight()
            print(moves)
        elif moves == [0,0,1,0]:
            print(f'right {i}:')
            right()
            print(moves)

        i += 1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()