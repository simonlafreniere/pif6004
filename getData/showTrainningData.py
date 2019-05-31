# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

balanced_train_data = np.load('training_data_balanced.npy', allow_pickle=True)
train_data = np.load('training_data.npy', allow_pickle=True)
df = pd.DataFrame(train_data)
bdf = pd.DataFrame(balanced_train_data)
print('-----------------data-------------------------')
print(Counter(df[1].apply(str)))
print('----------------------------------------------')
print('')
print('-------------balanced data--------------------')
print(Counter(bdf[1].apply(str)))
print('----------------------------------------------')
