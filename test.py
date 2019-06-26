import numpy as np
from PIL import ImageGrab
import cv2

x_pad = 271
y_pad = 236
box = (x_pad+1, y_pad+1, x_pad+805, y_pad+461)

class fullprint:
    'context manager for printing full numpy arrays'

    def __init__(self, **kwargs):
        kwargs.setdefault('threshold', np.inf)
        self.opt = kwargs

    def __enter__(self):
        self._opt = np.get_printoptions()
        np.set_printoptions(**self.opt)

    def __exit__(self, type, value, traceback):
        np.set_printoptions(**self._opt)

screen =  np.array(ImageGrab.grab(box))
lower_yellow = np.array([160,130,0], dtype = "uint16")
upper_yellow = np.array([255,255,65], dtype = "uint16")
yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
screen[yellow_mask != 0] = [255,255,255]
screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
screen = cv2.resize(screen, (80,46))
a = screen
#a = cv2.imread('8p.jpeg')

with fullprint():
    print(a)