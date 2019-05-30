import os
import os
import json
import scipy.misc
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="check which user..")
parser.add_argument("-u", "--user", nargs=1)

user = None


def initialisation():
    global user
    args = parser.parse_args()
    if args.user is None or args.user[0] == 'p':
        user = 'p'
    elif args.user[0] == 's':
        user = 's'


def main():
    initialisation()

    train_data = np.load('training_data_balanced.npy', allow_pickle=True)
    path = "./Modern_Car_Racing/train"
    with open('convert_config.' + user +'.json') as json_data_file:
        data = json.load(json_data_file)

    forward = int(data['forward'])
    brake = int(data['brake'])
    left = int(data['left'])
    right = int(data['right'])

    for i in train_data:
        if i[1] == [1, 0, 0, 0]:
            scipy.misc.imsave(path + '/left/' + str(left) + user + '.jpeg', i[0])
            left += 1
        if i[1] == [0, 0, 1, 0]:
            scipy.misc.imsave(path + '/right/' + str(right) + user + '.jpeg', i[0])
            right += 1
        if i[1] == [0, 0, 0, 1]:
            scipy.misc.imsave(path + '/brake/' + str(brake) + user + '.jpeg', i[0])
            brake += 1
        if i[1] == [0, 1, 0, 0]:
            scipy.misc.imsave(path + '/forward/' + str(forward) + user + '.jpeg', i[0])
            forward += 1

    data['forward'] = forward + 1
    data['brake'] = brake + 1
    data['left'] = left + 1
    data['right'] = right + 1

    with open('convert_config.' + user +'.json', 'w') as outfile:
        json.dump(data, outfile)

    os.remove("training_data.npy")
	
	
if __name__ == '__main__':
    main()