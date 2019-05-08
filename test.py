import cv2
import numpy as np
from PIL import ImageGrab

def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

def screenGrab():
    box = (320,305,350,355)
	
    while(True):
        firstScreen =  np.array(ImageGrab.grab(box))
        gray = cv2.cvtColor(firstScreen,cv2.COLOR_BGR2GRAY)
        (T, segm) = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
        gauss = cv2.GaussianBlur(segm,(5,5),0)
        edges = cv2.Canny(gauss,50,150,apertureSize = 3)
        lines = cv2.HoughLines(edges,1,np.pi/180, 200)
        cv2.imshow('window',cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()