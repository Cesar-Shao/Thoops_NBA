import os
import matplotlib.pyplot as plt
import pandas as pd


dir=os.path.abspath('.')

top_ls=[]
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




for i in top_ls:

    fig,axes=plt.subplots(2,1,gridspec_kw={'height_ratios':[1,1.7]},figsize=(20,10))
    player_pic=plt.imread(f'{dir}/input_data/player_pic/{i.strip()}.png')
    data_pic=plt.imread(f'{dir}/res/player_datatable/{i.strip()}.png')
    axes[0].imshow(player_pic)
    axes[1].imshow(data_pic)
    
    for ax in axes:
        ax.axis("off")
    
    
    plt.subplots_adjust(wspace=-10)
    
    plt.savefig(f'{dir}/res/player_data_pic/{i.strip()}.png')
    plt.close()



'''

for i in range(0,12):
    fig,axes=plt.subplots(1,2,gridspec_kw={'width_ratios':[1.4,1]},figsize=(20,10))
    radar_pic=plt.imread(f'{dir}/res/radar_T/{i+1}.png')
    court_pic=plt.imread(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/{i}.jpg')
    axes[0].imshow(court_pic)
    axes[1].imshow(radar_pic)
    
    for ax in axes:
        ax.axis("off")
    
    
    plt.subplots_adjust(wspace=0)
    
    plt.savefig(f'{dir}/res/court_radar_pic/{i}.png')
    plt.close()

'''