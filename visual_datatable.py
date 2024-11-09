import pandas as pd
import matplotlib.pyplot as plt
import os




dir=os.path.abspath('.')
pt=pd.read_csv(f"{dir}/input_data/NBA_playtype_2015-16.csv")




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
    try:
        
                
        data=pt.loc[pt['Player'].str.replace(' ','')==i.strip()].filter(like='Freq').fillna(0)
        df = pd.DataFrame(data)

        # 创建表格图片
        fig, ax = plt.subplots(figsize=(16, 4))  # 设置图片大小
        ax.axis('off')  # 隐藏坐标轴
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

        # 设置表格样式
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)

        # 保存表格图片
        #plt.show()
        plt.savefig(f'{dir}/res/player_datatable/{i.strip()}.png', bbox_inches='tight', pad_inches=0.5)

    except:
        print('!!!!!!!!!!no pic!!!!!!!!!!!!!!')
        

