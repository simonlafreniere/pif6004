from positionSensor import getPosition
import cv2

img = cv2.imread('image.jpg')
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = getPosition(RGB_img)
print(result)