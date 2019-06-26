from imageai.Prediction.Custom import CustomImagePrediction
import os
execution_path = os.getcwd()
import numpy as np
from PIL import ImageGrab
import cv2
from time import sleep
from directkeys import PressKey,ReleaseKey, W, A, S, D

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


def predict_actions(image) {

    result = [];
    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath(os.path.join(execution_path, "./models/model_ex-007_acc-0.587639.h5"))
    prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
    prediction.loadFullModel(num_objects=4)
    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, image), result_count=4)

    for eachPrediction, eachProbability in zip(predictions, probabilities):
	    result.add(eachPrediction + ":" + eachProbability)
	
    return result;
}
 
def left():
    PressKey(A)
    sleep(2)
    ReleaseKey(A)

def right():
    PressKey(D)
    sleep(2)
    ReleaseKey(D)

def forward():
    PressKey(W)
    sleep(2)
    ReleaseKey(W)

def release():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
	
def brake():
    PressKey(S)
    sleep(0.1)
    ReleaseKey(S)


def main():

    box = (x_pad+1, y_pad+1, x_pad+805, y_pad+461)
    i = 0
    while(True):
        screen =  np.array(ImageGrab.grab(box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,46))
        #cv2.imshow('',screen)
        predictionArray = predict_actions(screen)
		
        for actions in predictionArray {
		action = actions.split(':'))
        print(action[0]);
		print(action[1]);
		}
		
        if action == "left":
            print(f'left  {i}:')
            left()
        elif action == "forward":
            print(f'forward  {i}:')
            forward()
        elif action == "right":
            print(f'right {i}:')
            right()
        elif action == "brake":
            print(f'brake {i}:')
            brake()

        i += 1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()