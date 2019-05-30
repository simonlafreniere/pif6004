import os
import scipy.misc
import numpy as np

train_data = np.load('training_data_balanced.npy', allow_pickle=True)
path = "./Modern_Car_Racing/train"
forward = 5000
brake = 5000
left = 5000
right = 5000


for i in train_data:
    if(i[1] == [1,0,0,0]):
        scipy.misc.imsave(path + '/left/' + str(left)  + '.jpeg', i[0])
        left +=1
    if(i[1] == [0,0,1,0]):
        scipy.misc.imsave(path + '/right/' + str(right)  + '.jpeg', i[0])
        right +=1
    if(i[1] == [0,0,0,1]):
        scipy.misc.imsave(path + '/brake/' + str(brake)  + '.jpeg', i[0])
        brake +=1
    if(i[1] == [0,1,0,0]):
        scipy.misc.imsave(path + '/forward/' + str(forward)  + '.jpeg', i[0])
        forward +=1
