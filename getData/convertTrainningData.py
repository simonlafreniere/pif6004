import os
import json
import scipy.misc
import numpy as np

train_data = np.load('training_data_balanced.npy')
path = "./Modern_Car_Racing/train"
with open('convert_config.json') as json_data_file:
    data = json.load(json_data_file)
	
forward = int(data['forward'])
brake = int(data['brake'])
left = int(data['left'])
right = int(data['right'])

for i in train_data:
    if(i[1] == [1,0,0,0]):
        scipy.misc.imsave(path + '/left/p.' + str(left)  + '.jpeg', i[0])
        left +=1
    if(i[1] == [0,0,1,0]):
        scipy.misc.imsave(path + '/right/p.' + str(right)  + '.jpeg', i[0])
        right +=1
    if(i[1] == [0,0,0,1]):
        scipy.misc.imsave(path + '/brake/p.' + str(brake)  + '.jpeg', i[0])
        brake +=1
    if(i[1] == [0,1,0,0]):
        scipy.misc.imsave(path + '/forward/p.' + str(forward)  + '.jpeg', i[0])
        forward +=1
		
data['forward'] = forward
data['brake'] = brake
data['left'] = left
data['right'] = right

with open('convert_config.json', 'w') as outfile:
    json.dump(data, outfile)		