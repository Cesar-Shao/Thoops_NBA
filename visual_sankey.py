from pyecharts.charts import  Sankey
from pyecharts import options as opts
import pandas as pd
import os

# 定义一个函数，用于获取每行最大的三个数及其索引
def get_top_k(row,k=6,large=1):
    top_k = row.nlargest(k) if large==1 else row.nsmallest(k) # 获取最大的三个数
    indices = top_k.index.tolist()  # 获取最大的三个数的列索引
    values = top_k.values.tolist()  # 获取最大的三个数的值
    result = [(value, row.name, index) for value, index in zip(values, indices)]  # 存储值、行索引和列索引的元组
    return result


def DrawSankey(df,out_dir,k=6,large=1):
    nodes=[]
    for i in df.index:
        temp_dic={}
        temp_dic['name']=i
        nodes.append(temp_dic)
    for i in df.columns:
        temp_dic={}
        temp_dic['name']=i
        nodes.append(temp_dic)
    print(nodes)

    top_res = df.apply(get_top_k,args=(k,large), axis=1).tolist()
    temp_max=0
    for i in top_res:
        for j in i:
            if j[0]>temp_max:
                temp_max=j[0]

    linkes=[]
    for i in top_res:
        for j in i:
            temp_dic={}
            temp_dic['source']=j[1]
            temp_dic['target']=j[2]
            temp_dic['value']=j[0] #if large==1 else 1/j[0]
            linkes.append(temp_dic)

    for i in linkes:
        print(i)

    pic=(
        Sankey().add(
            '',#图例名称
            nodes,#传入节点数据
            linkes,#传入边和流量数据
            #设置透明度、弯曲度、颜色
            linestyle_opt=opts.LineStyleOpts(opacity=0.3,curve=0.5,color='source'),
            #标签显示位置
            label_opts=opts.LabelOpts(position='right'),
            #节点之间的距离
            node_gap=30,
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=f'large{k}' if large==1 else f'little{k}'))
    )
    
    output1=f'{out_dir}/large{k}.html'
    output2=f'{out_dir}/little{k}.html'
    pic.render(output1 if large==1 else output2)


if __name__=="__main__":
    dir=os.path.abspath('.')
    df=pd.read_csv(dir+"/res/top5/res_mean.csv").iloc[:-1,:]
    df = df.rename(columns={df.columns[0]: 'Type'})
    df=df.set_index('Type')
    
    sankey_dir=f'{dir}/res/sankey'
    if not os.path.exists(sankey_dir):
        os.makedirs(sankey_dir)
    for large in range(0,2):
        for k in range(3,7):
            DrawSankey(df,sankey_dir,k,large)