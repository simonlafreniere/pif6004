# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('training_data.npy')

lefts = []
rights = []
forwards = []
brakes = []
do_nothings = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1, 0, 0, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 0, 0]:
        forwards.append([img, choice])
    elif choice == [0, 0, 1, 0]:
        rights.append([img, choice])
    elif choice == [0, 0, 0, 1]:
        brakes.append([img, choice])
    elif choice == [0, 0, 0, 0]:
        do_nothings.append([img, choice])
    else:
        print('no matches')


forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

final_data = forwards + lefts + rights + brakes
shuffle(final_data)

np.save('training_data_v3.npy', final_data)
