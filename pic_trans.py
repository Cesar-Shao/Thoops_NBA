import os
from PIL import Image
import imageio
from skimage import io

dir=os.path.abspath('.')


for root,dirs,files in os.walk(dir+'/input_data/player_pic'):
    for i in files:
        if '.webp' in i:
            webp_pic=Image.open(f"{dir}/input_data/player_pic/{i}")
            webp_pic.save(f"{dir}/input_data/player_pic/{i.split('.')[0]}.png",'PNG')
        '''if '.avif' in i:
            avif_pic=Image.open(f"{dir}/input_data/player_pic/{i}")
            avif_pic.save(f"{dir}/input_data/player_pic/{i.clip('.')[0]}.png",'PNG')'''