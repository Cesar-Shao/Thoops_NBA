import numpy as np
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")


#⬇️⬇️得到thoop中每个component的topk个球员的playtype数据
def topk_type(pt,player,dir):
    topk=player.readlines()
    #res=pd.DataFrame()
    #new_row = pd.Series({'col1': 0, 'col2': 0})
    pt_list=[]
    tempt=pd.DataFrame()

    #⬇️⬇️为每个球员添加Type，1～12，不同于component0～11，因为后续有Dataframe补零
    type_num=0
    for i in topk:
        if("Component" in i.strip()):#读到新的Component处
            tempt['Type']=type_num
            pt_list.append(tempt)
            tempt=pd.DataFrame()
            type_num+=1
        else:
            tempt=tempt.append(pt.loc[pt['Player'].str.replace(' ','')==i.strip()]) #⬅️去掉球员名字空格
    tempt['Type']=type_num
    pt_list.append(tempt)

    pt_res_0=pd.DataFrame()
    for i in pt_list:
        pt_res_0=pd.concat([pt_res_0,i])
        #pt_res_0=pd.concat([pt_res_0,new_row])

    #⬇️⬇️尝试对top3～10个球员做处理，从中选择效果更好的
    for i in range(3,11):
        folder_name = f"{dir+'/res/'}top{i}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name) #创建一系列文件夹

        pt_res1=pt_res_0.iloc[:,0:2]
        pt_res2=pt_res_0.filter(like='Freq')

        pt_res=pd.concat([pt_res1,pt_res2],axis=1)
        #file_path = f'路径/{variable_name}.csv'
        pt_res.to_csv(f"{dir+'/res/'}top{i}/out.csv",index=False)

#########################################################################

def group_res(dir):

    #计算分组期望方差、输出csv
    for i in range(3,11):
        out_dir=f"{dir+'/res/'}top{i}"
        pt=pd.DataFrame(pd.read_csv(f"{out_dir+'/out.csv'}"))
        pt = pt.fillna(0)

        grouped = pt.groupby('Type').head(i) #分组并取每组前i个
        grouped = grouped.groupby('Type')
        #print(grouped)
        gp_mean=grouped.mean()
        #print(gp_mean)
        gp_var=grouped.var()
        all_mean=pt.mean()
        #print(all_mean)
        bt_var=((gp_mean - all_mean) ** 2).mean()
        #print(bt_var)
        #计算四个指标

        #gp_mean.to_csv(out_dir+'/gp_mean.csv')
        #gp_var.to_csv(out_dir+'/gp_var.csv')
        
        all_mean = all_mean.rename('all_mean')
        #all_mean.T.to_csv(out_dir+'/all_mean.csv')
        
        res_mean=pd.concat([gp_mean.T,all_mean],axis=1)
        #res_mean = res_mean.rename(index={res_mean.index[0]: 'Type'})
        res_mean.T.iloc[:,0:-1].to_csv(out_dir+'/res_mean.csv')
        #res_mean.T.to_csv(out_dir+'/res_mean.csv')
        
        bt_var=bt_var.rename('bt_var')
        #bt_var.to_csv(out_dir+'/bt_var.csv')
        
        res_var=pd.concat([gp_var.T,bt_var],axis=1)
        res_var.T.iloc[:,0:-1].to_csv(out_dir+'/res_var.csv')
        
        #all_mean.to_csv(out_dir+'/all_mean.csv')


def meanvar_filter(mean_df,var_df,ascend=True,headk=6):
    res=[]
    for i in mean_df.columns[1:]:
        mean_sorted=mean_df.iloc[:-1,:].sort_values(by=i,ascending=ascend)
        mean_sorted = mean_sorted.reset_index(drop=True)
        mean_top=mean_sorted.head(headk).iloc[:,0]
        for j in mean_top:
            tempt=[]
            if(var_df.loc[int(j)-1,i]<var_df.loc[var_df.index[-1],i]):
                tempt=[i,j,mean_sorted[mean_sorted.iloc[:,0]==j].index.values[0]+1,mean_df.loc[int(j)-1,i],var_df.loc[int(j)-1,i],mean_df.iloc[-1][i],var_df.iloc[-1][i]]
                res.append(tempt)
    return(res)



if __name__=="__main__":
    
    dir=os.path.abspath('.')
    pt_pre=pd.DataFrame(pd.read_csv(dir+'/input_data/NBA_playtype_2015-16.csv'))
    pt=pt_pre.iloc[:,1:2].join(pt_pre.iloc[:,3:])#去掉ID列
    player=open(dir+'/input_data/components/All_DefensiveDistance_nnp_rank10/topk.txt')
    #player=open(dir+'/input_data/components/All_PERIOD_nnp_rank10/topk.txt')
    topk_type(pt,player,dir)
    group_res(dir)
    
    for i in range(3,15):
        out_dir=f"{dir+'/res/'}top{i}"
        mean_df=pd.DataFrame(pd.read_csv(out_dir+'/res_mean.csv'))
        var_df=pd.DataFrame(pd.read_csv(out_dir+'/res_var.csv'))
        dic_great=meanvar_filter(mean_df,var_df,ascend=False)
        dic_little=meanvar_filter(mean_df,var_df,ascend=True)
        
        df_great=pd.DataFrame(dic_great,columns=['type','component','rank','mean','var','mean_all','var_group'])
        df_little=pd.DataFrame(dic_little,columns=['type','component','rank','mean','var','mean_all','var_group'])
        
        #print(df_great)
        #print(df_little)
        
        df_great.to_csv(out_dir+'/great6mean_var.csv',index=False)
        df_little.to_csv(out_dir+'/little6mean_var.csv',index=False)