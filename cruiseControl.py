import re
import threading

import cv2
from time import sleep
import numpy as np
from PIL import ImageGrab, Image
from pynput.keyboard import Key, Controller, Listener
import pynput.keyboard as pynput_keyboard

keyboard = Controller
quit_now = False


def forward():
    keyboard.press(Key.up)
    sleep(0.2)
    keyboard.release(Key.up)


# def release():
#     ReleaseKey(W)
#     ReleaseKey(A)
#     ReleaseKey(D)
#     ReleaseKey(S)


def brake():
    keyboard.press(Key.space)
    sleep(0.1)
    keyboard.release(Key.space)


def screen_grab():
    box = (327, 300, 328, 360)
    kernel = np.ones((5, 5), np.uint8)
    speed = 0.0
    last_speed = 0.0
    while True:
        image = np.array(ImageGrab.grab(box))
        # convert red to black
        lower_red = np.array([220, 0, 0], dtype="uint16")
        upper_red = np.array([240, 10, 50], dtype="uint16")
        red_mask = cv2.inRange(image, lower_red, upper_red)
        image[red_mask != 0] = [0, 0, 0]
        # image = cv2.resize(image, (120,200))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (T, seg) = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY_INV)
        gauss = cv2.GaussianBlur(seg, (5, 5), 0)
        edges = cv2.Canny(gauss, 100, 200, apertureSize=3)
        dilation = cv2.dilate(edges, kernel, iterations=5)
        erosion = cv2.erode(dilation, kernel, iterations=6)
        for index, x in np.ndenumerate(erosion):
            if x == 255:
                try:
                    index = re.sub('[(),0]', '', str(index))
                    index = float(index)
                    speed = abs((index - 44)*1.45)
                    if abs(speed - last_speed) < 20:
                        last_speed = speed
                        print(speed)
                    else:
                        print(last_speed)
                except ValueError as e:
                    print(last_speed, e)

        if speed < 35 and last_speed < 35:
            forward()
        # if(speed>40 and lastSpeed>40):
        #     release()
        # don't care just do nothing..
        if speed > 55 and last_speed > 55:
            brake()

        if quit_now:
            cv2.destroyAllWindows()

            break


def on_press(key):
    if key == pynput_keyboard.KeyCode.from_char('q'):
        global quit_now
        quit_now = True


def listener_thread():
    # Collect events until released
    with Listener(on_press=on_press) as listener:
        listener.join()


def main():
    # threading the keyboard listener
    threading.Thread(target=listener_thread).start()
    screen_grab()


if __name__ == '__main__':
    main()
