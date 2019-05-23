from positionSensor import getPosition
import cv2
import  numpy as np
from PIL import ImageGrab


box = box = (77 + 1, 166 + 1, 77 + 917, 166 + 546)

img = np.array(ImageGrab.grab(box))
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = getPosition(RGB_img)
print(result)
