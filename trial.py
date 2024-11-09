import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


dir=os.path.abspath('.')

for i in range(0,12):
    coeff=pd.read_csv(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/coefficient_csv/component{i}.csv')
    for x in range(1,6):
        print('|',coeff.iloc[x-1,0],'|')
    print('----------------------------------')