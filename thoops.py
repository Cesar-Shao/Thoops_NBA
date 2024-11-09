import numpy as np
import pandas as pd
from tensorly.decomposition import parafac, non_negative_parafac
from corcondia import corcondia_3d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from yellowbrick.cluster import KElbowVisualizer, SilhouetteVisualizer
from tqdm import tqdm
import math
import os

from utils import *

dic=os.path.abspath('.')+'/'


def MakeTensor(only_train_set, attribute):
    '''
        Convert csv to shot chart
    '''
    partition = {
        'PERIOD': [1, 2, 3, 4],
        'ShotClock': [7.281, 12.8332, 18.6505],
        'DefensiveDistance': [3.9389, 8.0847, 14.5381]
    }[attribute]
    partition.append(math.inf)

    print('Loading shots')
    shots_file = 'input_data/shots_extended2.csv'
    shots = pd.read_csv(dic+shots_file)

    if only_train_set:
        game_ids = [int(x.split('/')[-2][2:]) for x in open('split/train.txt')]
        game_ids = list(set(game_ids))
        shots = shots[shots['GAME_ID'].isin(game_ids)]

    #print(len(shots))

    shots['LOC_X'] = shots['LOC_X'] / 10
    shots['LOC_Y'] = shots['LOC_Y'] / 10


    print('Determining area indices')
    shots['area'] = shots.apply(lambda row: area_id[area_name(row[['LOC_X', 'LOC_Y']])], axis=1)
    shots.loc[shots.PERIOD >= 5, 'PERIOD'] = 5

    players = {}
    for i, row in pd.read_csv(f'{dic}/input_data/players.csv').iterrows():
        players[row['UnifiedPlayerID']] = row['playerid']

    print('Number of players:', len(players))

    def create_tensor(shots):
        shots = shots[shots[attribute] <= 24]
        X = []
        for player in tqdm(range(len(players))):
            player_id = players[player]
            p_shots = shots[shots['PLAYER_ID'] == player_id]
            
            area = p_shots['area'].values
            att = p_shots[attribute].values
            att_ = np.zeros_like(att)
            for i in range(len(partition) - 1, -1, -1):
                att_[att <= partition[i]] = i
            A = np.zeros((13, len(partition)))
            for i in range(13):
                for j in range(len(partition)):
                    #A[i, j] = ((area == i) * (att_ == j)).sum()
                    #SJC:转换数据为百分比
                    A[i, j] = (((area == i) * (att_ == j)).sum())/p_shots.shape[0]
            print('sum:',np.sum(A))
            if not (p_shots.empty):
                X.append(A)
        return np.stack(X)

    os.makedirs('data', exist_ok=True)
    np.save(f'data/{"Train" if only_train_set else "All"}_{attribute}_X_made.npy', create_tensor(shots[shots['SHOT_MADE_FLAG'] == 1]))
    # np.save('X_miss.npy', create_tensor(shots[shots['SHOT_MADE_FLAG'] == 0]))

def Decompose(only_train_set, attribute, n_components=12):
    '''
        Tensor Decomposition
    '''
    tensor_fn = f'data/{"Train" if only_train_set else "All"}_{attribute}_X_made.npy'
    X = np.load(tensor_fn)
    players = pd.read_csv(f'{dic}/input_data/players.csv')

    weight, factor = non_negative_parafac(X, rank = n_components, n_iter_max=1000)
    
    save_path = f'input_data/components/{"Train" if only_train_set else "All"}_{attribute}_nnp_rank{n_components}'
    os.makedirs(save_path, exist_ok=True)

    out = open(f'{save_path}/topk.txt', 'w')

    for i in range(n_components):
        w = factor[1][:, i]
        w_t = factor[2][:, i]
        draw_court_weights(w, w_t, fn=f'{save_path}/{i}.jpg')
        out.write(f'Component {i}:\n')
        sort_idx = np.argsort(factor[0][:, i])[::-1]
        for j in range(10):
            idx = sort_idx[j]
            name = players[players.UnifiedPlayerID == idx].playername.values[0]
            out.write(f'{name}\n')
            #print("name:::",players[players.UnifiedPlayerID == idx].playername.values[0])
        out.write('\n')
    out.close()

    np.savez(tensor_fn.replace('.npy', f'_decompose_rank{n_components}.npz'), A=factor[0], B=factor[1], C=factor[2])

    recover = (factor[0][:,None,None,:] * factor[1][None,:,None,:] * factor[2][None,None,:,:]).sum(-1)
    loss = ((X - recover) ** 2).sum()
    print('Loss', loss)
    with open(f'{save_path}/loss.txt', 'w') as f:
        f.write('%.4f'%loss)
        f.close()

def Cluster(only_train_set, attribute, rank, n_clusters):
    '''
        Clustring the resulted player embeddings
    '''
    fn = f'data/{"Train" if only_train_set else "All"}_{attribute}_X_made_decompose_rank{rank}.npz'
    data = np.load(fn)['A']
    players = pd.read_csv(f'{dic}/input_data/players.csv')

    print('Clustering')
    clusters = KMeans(n_clusters=n_clusters, max_iter=300, n_init=10).fit(data)
    labels = clusters.labels_
    centers = clusters.cluster_centers_
    np.savez(fn.replace('.npz', f'_cluster{n_clusters}.npz'), labels=labels, centers=centers)

    player_info = []
    for i in range(len(labels)):
        label = labels[i]
        player_info.append({
            'id': i,
            'name': players[players.UnifiedPlayerID == i].playername.values[0],
            'group': label,
            'Dis2Center': np.sqrt(((data[i] - centers[label]) ** 2).sum())
        })
    df = pd.DataFrame(player_info)
    df.to_csv(fn.replace('.npz', f'_cluster{n_clusters}.csv'), index=False)

    dominant = data.argmax(-1)
    cnt = np.zeros((n_clusters, rank), dtype=int)
    for i in range(len(labels)):
        cnt[labels[i], dominant[i]] += 1
    out = open(fn.replace('.npz', f'_cluster{n_clusters}.txt'), 'w')
    for i in range(n_clusters):
        for j in range(rank):
            out.write(str(cnt[i, j]) + '\t')
        out.write('\n')
    out.close()

    print('T-SNE')
    tsne = TSNE(n_components=2, init='random', n_iter=2000)
    positions = tsne.fit_transform(data)

    color_map = ['r', 'g', 'b', 'darkviolet', 'gray', 'cyan', 'black']
    for i in range(positions.shape[0]):
        plt.scatter(positions[i, 0], positions[i, 1], c=color_map[labels[i]], linewidths=0, alpha=0.5)
    plt.savefig(fn.replace('.npz', f'_cluster{n_clusters}.jpg'))

#确定最佳的聚类数量
def elbow(only_train_set, attribute, rank):
    fn = f'data/{"Train" if only_train_set else "All"}_{attribute}_X_made_decompose_rank{rank}.npz'
    data = np.load(fn)['A']
    km = KMeans(init='k-means++', n_init=10, max_iter=300, random_state=0)
    visualizer = KElbowVisualizer(km, k=(2,21))
    visualizer.fit(data)        # Fit the data to the visualizer
    visualizer.show()

#绘制loss- num(component)的关系
def plot_loss(attribute):
    y = []
    for i in range(1, 21):
        fn = f'input_data/components/All_{attribute}_nnp_rank{i}/loss.txt'
        for line in open(fn):
            y.append(float(line.strip()))
    x = list(range(1, 21))
    plt.plot(x, y)
    plt.xticks(range(1, 21))  # 设置x轴刻度值为1到20
    plt.yticks()  # 根据数据自动设置y轴刻度值
    plt.savefig(f'input_data/components/{attribute}_loss.jpg')
    plt.close()

def determine_n_components(attribute):
    tensor_fn = f'data/All_{attribute}_X_made.npy'
    X = np.load(tensor_fn)
    y = []
    for i in range(1, 21):
        #y.append(corcondia_3d(X, k=i, non_negative=True, n_iter_max=1000))
        y.append(corcondia_3d(X, k=i, n_iter_max=1000))
        print(i, y[-1])
    x = list(range(1, 21))
    plt.plot(x, y)
    plt.savefig(f'input_data/components/{attribute}_corcondia.jpg')
    plt.close()
    
def find_top_players_coefficients(attribute, n_components):
    tensor_fn = f'data/All_{attribute}_X_made_decompose_rank{n_components}.npz'
    save_path = f'input_data/components/All_{attribute}_nnp_rank{n_components}'
    A = np.load(tensor_fn)['A']
    players = pd.read_csv(f'{dic}/input_data/players.csv')
    out = open(f'{save_path}/topk_max_coefficient.txt', 'w')

    for i in range(n_components):
        out.write(f'Component {i}:\n')
        coefficients={}
        sort_idx = np.argsort(A[:, i])[::-1]
        for j in range(5):
            idx = sort_idx[j]
            name = players[players.UnifiedPlayerID == idx].playername.values[0]
            coefficients[name]=[]
            for c in range(n_components):
                coefficients[name].append(A[idx,c])
            out.write(f'{name}\t{A[idx, i]}\n')
        out.write('\n')
    
        df_coeffi=pd.DataFrame(coefficients).T
        if not os.path.exists(f'{save_path}/coefficient_csv'):
            os.mkdir(f'{save_path}/coefficient_csv')
        df_coeffi.to_csv(f'{save_path}/coefficient_csv/component{i}.csv')
    out.close()


if __name__ == '__main__':
    only_train_set = False
    attribute = 'DefensiveDistance'
    #MakeTensor(only_train_set, attribute)
    
    
    '''for i in range(3,15):
        Cluster(only_train_set, attribute, rank=12, n_clusters=i)'''

        
    for i in range(1,21):
        Decompose(only_train_set, attribute, n_components=i)
        find_top_players_coefficients(attribute, n_components=i)
        
    #plot_loss(attribute)
    elbow(only_train_set, attribute, rank=12)