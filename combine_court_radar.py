import os
import matplotlib.pyplot as plt
dir=os.path.abspath('.')

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

