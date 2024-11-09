import os
import pandas as pd

dir=os.path.abspath('.')
top_ls=[]
pic_ls=[]

folder_path=dir+"/input_data/player_pic"
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        pic_ls.append(file_name)

for i in range(len(pic_ls)):
    pic_ls[i]=pic_ls[i].split('.')[0]

with open(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/topk.txt') as topk:
    '''for line in topk.readlines():
        if not 'Component' in line:
            print(line.strip())'''
    while(1):
        a=topk.readline()
        if(a):
            if "Component" in a:
                for i in range(5):
                    top_ls.append(topk.readline().strip())
        else:
            break

top_ls=set(top_ls)
pic_ls=set(pic_ls)

find=top_ls-pic_ls
print(find)