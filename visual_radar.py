import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def find_top_n_indices(lst,n):#找出最显著的n个点
    sorted_indices = sorted(enumerate(lst), key=lambda x: x[1][1], reverse=True)
    top_n_indices = [idx for idx, _ in sorted_indices[:n]]
    return top_n_indices


def radar(data):
    # 转换数据
    categories = [i[0] for i in data]
    values = np.array([i[1] for i in data])
    N = len(categories)

    # 绘制图形
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, polar=True)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    values = np.concatenate((values, [values[0]]))
    theta = np.concatenate((theta, [theta[0]]))
    ax.plot(theta, values, color='r', linewidth=2, linestyle='-', marker='o', markersize=10)
    ax.fill(theta, values, facecolor='r', alpha=0.1)
    
    # 添加方向标签
    ax.set_xticks(theta[:-1])
    ax.set_xticklabels([x[0] for x in data])
    
    idxls=find_top_n_indices(data,5)

    '''print(idxls)
    print(values)
    print(categories)'''
    for i in idxls:
        angle = i / float(N) * 2 * np.pi
        ax.text(angle, values[i], categories[i], ha='center', va='center')
    
    # 显示图形
    #plt.show()


#for topk in range(3,11):
topk=5
dic=os.path.abspath('.')+f"/res/top{topk}"
folder_name = f"{dic+'/visualize_pic/radar_T'}"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
#pt=pd.DataFrame(pd.read_csv(dic+'/group_10_defense/res_mean_norm.csv'))
pt=pd.DataFrame(pd.read_csv(dic+'/res_mean.csv'))
pt = pt.fillna(0)
pt.index=pt.iloc[:,0]

for i in range(len(pt.index)):
    type_data = pt.iloc[i, 1:]
    data = []
    for j in range(len(type_data)):
        data.append((type_data.index[j], type_data.values[j]))
    filename = f"{dic}/visualize_pic/radar_T/{pt.index[i]}.png"  # 使用行索引作为文件名的一部分
    radar(data)
    plt.savefig(filename)
    plt.close()  # 关闭图形，释放内存


#创建多幅雷达图叠加的结合图
#⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️

# 创建雷达图
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

# 遍历每条曲线
for i in range(len(pt.index)):
    type_data = pt.iloc[i, 1:]
    data = []
    for j in range(len(type_data)):
        data.append((type_data.index[j], type_data.values[j]))

    # 将数据转换为极坐标系下的角度和距离
    angles = np.linspace(0, 2 * np.pi, len(data), endpoint=False)
    values = [x[1] for x in data]

    # 将最后一个点与第一个点相连，形成闭合曲线
    angles = np.concatenate((angles, [angles[0]]))
    values = np.concatenate((values, [values[0]]))

    # 绘制雷达图
    ax.plot(angles, values, label=pt.index[i])

# 添加方向标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels([x[0] for x in data])

# 添加图例
ax.legend()

# 保存雷达图
plt.savefig(f"{dic}/visualize_pic/radar_T/radar_combined.png")
plt.close()  # 关闭图形，释放内存
'''
import plotly.graph_objects as go

# 创建雷达图的数据
data = []
for i in range(len(pt.index)):
    type_data = pt.iloc[i, 1:]
    values = type_data.values.tolist()
    values.append(values[0])  # 将最后一个点与第一个点相连，形成闭合曲线
    data.append(go.Scatterpolar(
        r=values,
        theta=type_data.index.tolist() + [type_data.index[0]],
        fill='toself',
        name=pt.index[i]
    ))

# 创建布局
layout = go.Layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

# 创建图表对象
fig = go.Figure(data=data, layout=layout)

# 显示图表
fig.show()

'''
