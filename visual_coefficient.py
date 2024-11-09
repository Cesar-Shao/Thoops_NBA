import os
import matplotlib.pyplot as plt
import pandas as pd


dir=os.path.abspath('.')


#⬇️⬇️⬇️找出每个component系数最大的前五个
top_ls=[]
with open(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/topk.txt') as topk:
    while(1):
        a=topk.readline()
        if(a):
            if "Component" in a:
                for i in range(5):
                    top_ls.append(topk.readline().strip())
        else:
            break



for n in range(0,12):
    coeff=pd.read_csv(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/coefficient_csv/component{n}.csv')
    coeff=coeff.round(4)
    plt.figure(figsize=(15,8))
    grid = plt.GridSpec(7,14)
    for x in range(1,6):
        player_pic=plt.imread(f'{dir}/input_data/player_pic/{coeff.iloc[x-1,0]}.png')
        plt.subplot(grid[x, 1]).imshow(player_pic)
        plt.axis('off')
    for y in range(2,14):
        court_pic=plt.imread(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/{y-2}.jpg')
        plt.subplot(grid[0, y]).imshow(court_pic)
        plt.axis('off')
    ax = plt.subplot(grid[0,0:2])
    ax.axis('off')
    for i, row in enumerate(coeff.values):
        for j, value in enumerate(row):
            
            ax = plt.subplot(grid[i+1, j]) if(j==0) else plt.subplot(grid[i+1, j+1])
            ax.axis('off')  # 关闭坐标轴
            ax.text(0.5, 0.5, str(value), ha='center', va='center')
    plt.savefig(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/coefficient_csv/component{n}.png',dpi=200)








'''
#⬇️⬇️⬇️对其中的每一个画图
for i in top_ls:

    # 创建一个2行2列的网格布局
    plt.figure(figsize=(15,8))
    grid = plt.GridSpec(7,14)
    player_pic=plt.imread(f'/Users/cesar/Downloads/JamesHarden.png')
    data_pic=plt.imread(f'{dir}/res/player_datatable/{i.strip()}.png')
    
    for x in range(1,6):
        plt.subplot(grid[x, 1]).imshow(player_pic)
        plt.axis('off')
    for y in range(2,14):
        plt.subplot(grid[0, y]).imshow(player_pic)
        plt.axis('off')

    ax = plt.subplot(grid[0,0:2])
    ax.axis('off')
    

    coeff=pd.read_csv(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/coefficient_csv/component3.csv')
    coeff=coeff.round(4)
    for i, row in enumerate(coeff.values):
        for j, value in enumerate(row):
            
            ax = plt.subplot(grid[i+1, j]) if(j==0) else plt.subplot(grid[i+1, j+1])
            ax.axis('off')  # 关闭坐标轴
            ax.text(0.5, 0.5, str(value), ha='center', va='center')
    
    
    #plt.show()
    plt.savefig('/Users/cesar/Downloads/9_8.png',dpi=200)'''