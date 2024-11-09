import numpy as np
import pandas as pd
import os

dir=os.path.abspath('.')
res=[]
for i in range(3,11):
    out_dir=f"{dir+'/res/'}top{i}"
    great=pd.read_csv(out_dir+'/great6mean_var.csv')
    little=pd.read_csv(out_dir+'/little6mean_var.csv')
    
    great_num=great.shape[0]
    little_num=little.shape[0]
    
    res.append([i,great_num,little_num])
    
with open(dir+'/res/num.txt','w') as num_f:
    for i in res:
        a=f"前{i[0]}个的统计结果：great6有{i[1]}个，little6有{i[2]}个，共{i[1]+i[2]}个"
        num_f.write(a+'\n')
    