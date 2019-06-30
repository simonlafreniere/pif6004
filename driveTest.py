from speedSensor import getSpeed
from PIL import ImageGrab
import numpy as np
import settings
import cv2
import os
from time import sleep
from pynput.keyboard import Key, Controller
import threading

x_pad = settings.x_pad
y_pad = settings.y_pad
width = settings.width
height = settings.height
box = (x_pad + 1, y_pad + 1, x_pad + width, y_pad + height)
keyboard = Controller()
right_pressed = False
left_pressed = False
forward_pressed = False
brake_pressed = False

def predict_actions(image):

    predictionArray = []
    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath(os.path.join(execution_path, "./models/model_ex-007_acc-0.587639.h5"))
    prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
    prediction.loadModel(num_objects=4)
    predictions, probabilities = prediction.predictImage(image, result_count=4, input_type="array")
    
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        predictionArray.append(eachPrediction + ":" + eachProbability)
    
    return predictionArray


def analyzePrediction(predictionArray):
    for eachPrediction in predictionArray:
        prediction = eachPrediction.split(":")
	# todo - decide what to return after analyzing probalities
    return prediction[0]

def right():
    global right_pressed
    right_pressed = True

    # make sure we don't fight between threads
    keyboard.release(Key.left)
    keyboard.press(Key.right)
    sleep(0.1)
    keyboard.release(Key.right)

    right_pressed = False


def left():
    global left_pressed
    left_pressed = True

    keyboard.release(Key.right)
    keyboard.press(Key.left)
    sleep(0.1)
    keyboard.release(Key.left)

    left_pressed = False


def forward():
    speed = getSpeed()
	if(speed < 35):
        global forward_pressed
        forward_pressed = True
	
        keyboard.release(Key.down)
        keyboard.press(Key.up)
        sleep(0.4)
        keyboard.release(Key.up)


def release():
    # on sait que c'est up, les autres sont toujours released..
    keyboard.release(Key.up)


def brake():
    global brake_pressed
    brake_pressed = True
    # make sure we don't accelerate anymore..
    keyboard.release(Key.up)
    keyboard.press(Key.down)
    sleep(0.2)
    keyboard.release(Key.down)


def main():
    last_speed = 0

    while True:
        screen =  np.array(ImageGrab.grab(box))
        lower_yellow = np.array([160,130,0], dtype = "uint16")
        upper_yellow = np.array([255,255,65], dtype = "uint16")
        yellow_mask = cv2.inRange(screen, lower_yellow, upper_yellow)
        screen[yellow_mask != 0] = [255,255,255]
        screen = np.stack([rgb2gray(screen[i]) for i in range(screen.shape[0])])
        screen = cv2.resize(screen, (80,46))
        predictionArray = predict_actions(screen)
        action = analyzePrediction(predictionArray)
        
        if action == "left":
            if not left_pressed:
                threading.Thread(target=left).start()
        if action == "right":
            if not right_pressed:
                threading.Thread(target=right).start()
        if action == "forward":
            if not forward_pressed:
                threading.Thread(target=forward).start()
        if action == "brake":
            if not brake_pressed:
                threading.Thread(target=brake).start()


if __name__ == '__main__':
    main()
