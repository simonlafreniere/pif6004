import os
import scipy.misc
import numpy as np

train_data = np.load('training_data_balanced.npy')
path = "./Modern_Car_Racing/train"
forward = 0
brake = 0
left = 0
right = 0



for i in train_data:
    if(i[1] == [1,0,0,0]):
        scipy.misc.imsave(path + '/left/' + str(left)  + '.tif', i[0])
        left +=1
    if(i[1] == [0,0,1,0]):
        scipy.misc.imsave(path + '/right/' + str(right)  + '.tif', i[0])
        right +=1
    if(i[1] == [0,0,0,1]):
        scipy.misc.imsave(path + '/brake/' + str(brake)  + '.tif', i[0])
        brake +=1
    if(i[1] == [0,1,0,0]):
        scipy.misc.imsave(path + '/forward/' + str(forward)  + '.tif', i[0])
        forward +=1
