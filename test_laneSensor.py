from laneSensor import findLanes
import cv2

img = cv2.imread('lanetest.jpg')
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
m1, m2 = findLanes(RGB_img)
print(m1,m2)
