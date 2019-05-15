from PIL import ImageGrab
import numpy as np
import cv2
import os
import time
from numpy import ones,vstack
from numpy.linalg import lstsq
from pynput.keyboard import Key, Controller
from statistics import mean

'''
All coordinates assume a screen resolution of 1366x768, and Chrome 
maximized with the Bookmarks Toolbar enabled.

x_pad = 271
y_pad = 236
Play area =  x_pad+1, y_pad+1, x_pad+805, y_pad+461
'''

# Globals
# ------------------
 
x_pad_pat = 271
y_pad_pat = 236
x_pad_decal_pat = x_pad_pat + 805
y_pad_decal_pat = y_pad_pat + 461
x_pad_sim = 230
y_pad_sim = 350
x_pad_decal_sim = x_pad_sim + 1676
y_pad_decal_sim = y_pad_sim + 912

x_pad = 0
y_pad = 0
x_pad_decal = 0
y_pad_decal = 0

keyboard = Controller()


def process_img(image):
    original_image = image
    # convert yellow lines to white lines
    lower_yellow = np.array([160, 130, 0], dtype="uint16")
    upper_yellow = np.array([255, 255, 65], dtype="uint16")
    yellow_mask = cv2.inRange(image, lower_yellow, upper_yellow)
    image[yellow_mask != 0] = [255, 255, 255]
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]], np.int32)
    processed_img = roi(processed_img, [vertices])
    '''
    more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
                                         rho   theta   thresh  min length, max gap:
    '''
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,      20,       15)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1,m2 = draw_lanes(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
        pass

    return processed_img, original_image, m1, m2


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):

    # if this fails, go with some default line
    try:
        '''
        finds the maximum y value for a lane marker 
        (since we cannot assume the horizon will always be at the same point.)
        '''
        ys = []  
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                '''
                These four lines:
                modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                Used to calculate the definition of a line, given two sets of coords.
                '''
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                a = vstack([x_coords, ones(len(x_coords))]).T
                m, b = lstsq(a, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]
            
            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]
            else:
                for other_ms in final_lanes_copy:
                    if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                        if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                            final_lanes[other_ms].append([m, b, line])
                            break
                    else:
                        final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))

    # if this fails, go with some default line
    try:
        '''
        finds the maximum y value for a lane marker 
        (since we cannot assume the horizon will always be at the same point.)
        '''
        ys = []  
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                ''' 
                These four lines:
                modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                Used to calculate the definition of a line, given two sets of coords.
                '''
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                a = vstack([x_coords, ones(len(x_coords))]).T
                m, b = lstsq(a, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]
            
            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]
                
            else:
                for other_ms in final_lanes_copy:
                    if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                        if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                            final_lanes[other_ms].append([m, b, line])
                            break
                    else:
                        final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))


def left():
    keyboard.press(Key.left)
    keyboard.release(Key.left)


def right():
    keyboard.press(Key.right)
    keyboard.release(Key.right)


def brake():
    keyboard.press(Key.down)
    keyboard.release(Key.down)


def screen_grab():
    last_time = time.time()
    box = (x_pad+1, y_pad+1, x_pad_decal, y_pad_decal)
    while True:
        # PressKey(W)
        screen = np.array(ImageGrab.grab(box))
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen,original_image, m1, m2 = process_img(screen)
        cv2.imshow('window',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

        if m1 < 0 and m2 < 0:
            right()
        elif m1 > 0 and m2 > 0:
            left()
        elif m1 > 0 and m2 < 0:
            '''kind of do nothing, we will let the cruise control deal with acceleration
            straight()'''
        else:
            brake()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def initialisation():
    global x_pad, y_pad, x_pad_decal, y_pad_decal
    x_pad = x_pad_pat
    y_pad = y_pad_pat
    x_pad_decal = x_pad_decal_pat
    y_pad_decal = y_pad_decal_pat


def main():
    initialisation()
    screen_grab()


if __name__ == '__main__':
    main()
