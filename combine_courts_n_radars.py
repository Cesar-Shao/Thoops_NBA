import os
import matplotlib.pyplot as plt
dir=os.path.abspath('.')

plt.figure(figsize=(8,9))
grid=plt.GridSpec(4,3)
for i in range(0,12):
    court_pic=plt.imread(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/{i}.jpg')
    plt.subplot(grid[i//3,i%3]).imshow(court_pic)
    plt.axis('off')

plt.subplots_adjust(hspace=-0.5, wspace=0)
plt.savefig(f'{dir}/input_data/components/All_DefensiveDistance_nnp_rank12/combined_courts.jpg',dpi=300)







plt.figure(figsize=(9,10))
grid=plt.GridSpec(4,3)
for i in range(0,12):
    radar_pic=plt.imread(f'{dir}/res/radar_T/{i+1}.png')
    plt.subplot(grid[i//3,i%3]).imshow(radar_pic)
    plt.axis('off')

plt.subplots_adjust(hspace=0, wspace=0)
plt.savefig(f'{dir}/res/radar_T/combined_radar.png',dpi=400)




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