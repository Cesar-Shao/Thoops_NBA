import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


dir=os.path.abspath('.')

# 创建一个3D图形对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 定义立方体的八个顶点坐标
vertices = [
    [0, 0, 0],
    [12, 0, 0],
    [12, 4, 0],
    [0, 4, 0],
    [0, 0, 5],
    [12, 0, 5],
    [12, 4, 5],
    [0, 4, 5]
]

# 定义立方体的面
faces = [
    [vertices[0], vertices[1], vertices[2], vertices[3]],
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[1], vertices[2], vertices[6], vertices[5]],
    [vertices[2], vertices[3], vertices[7], vertices[6]],
    [vertices[3], vertices[0], vertices[4], vertices[7]],
    [vertices[4], vertices[5], vertices[6], vertices[7]]
]

# 绘制立方体的面
for face in faces:
    poly = Poly3DCollection([face], alpha=0.9, linewidths=1, edgecolors='black')
    poly.set_facecolor('lightblue')
    ax.add_collection3d(poly)

# 绘制立方体的其他面
for i in range(0, 12):
    for j in range(0, 4):
        for k in range(0, 5):
            for face in faces:
                x = [v[0] + i*12 for v in face]
                y = [v[1] + j*4 for v in face]
                z = [v[2] + k*5 for v in face]
                poly = Poly3DCollection([list(zip(x, y, z))], alpha=0.9, linewidths=1, edgecolors='black')
                poly.set_facecolor('lightblue')
                ax.add_collection3d(poly)

# 设置坐标轴范围
ax.set_xlim([0, 144])#12*12
ax.set_ylim([0, 16])#4*4
ax.set_zlim([0, 25])#5*5


ax.set_xticks([0,12,24,36,48,60,72,84,96,108,120,132,144])  # 设置x轴刻度的位置
ax.set_xticklabels(['area1','area2','area3','...','...','...','...','...','...','...','...','area12',' '])  # 设置x轴刻度的标签

ax.set_yticks([0, 4, 8, 12, 16])  # 设置y轴刻度的位置
ax.set_yticklabels([ ' ',' ','Quater1', '...... ', 'Quater4'])  # 设置y轴刻度的标签

ax.set_zticks([0, 5, 10, 15, 20, 25])  # 设置z轴刻度的位置
ax.set_zticklabels([' ','Player1', 'Player2', 'Player3', 'Player4', 'Player5'])  # 设置z轴刻度的标签

ax.tick_params(axis='x', rotation=45)
ax.tick_params(axis='y', rotation=5)



'''ax.set_xlabel('投篮区域')
ax.set_ylabel('节次')
ax.set_zlabel('球员')'''


# 设置坐标轴长宽比
ax.set_box_aspect([12, 4, 5])

# 显示图形
#ax.axis('off')
#plt.show()
plt.savefig(f'{dir}/paper_visual/cube_1.png',dpi=300)
