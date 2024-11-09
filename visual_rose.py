import os
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts



dir=os.path.abspath('.') 
print(dir)
df=pd.read_csv(dir+"/res/top5/res_mean.csv").iloc[:-1,:]
df = df.rename(columns={df.columns[0]: 'Type'})
rose_dir=f'{dir+"/res/rose"}'
os.makedirs(rose_dir)
df=df.set_index('Type')
for i in df.index:
    tempt=df.loc[i,:]
    print(tempt.index)
    print(tempt.values)
    
    v=tempt.index.tolist()
    d=tempt.values.tolist()
    #v = tempt['疫情地区'].values.tolist()
    #d = tempt['累计'].values.tolist()

    color_series = ['#FAE927', '#E9E416', '#C9DA36', '#9ECB3C', '#6DBC49',
                    '#37B44E', '#3DBA78', '#14ADCF', '#209AC9', '#1E91CA',
                    '#2C6BA0', '#2B55A1', '#2D3D8E', '#44388E', '#6A368B'
                                                                '#7D3990', '#A63F98', '#C31C88', '#D52178', '#D5225B',
                    '#D02C2A', '#D44C2D', '#F57A34', '#FA8F2F', '#D99D21',
                    '#CF7B25', '#CF7B25', '#CF7B25']
    # 实例化Pie类
    pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
    # 设置颜色
    pie1.set_colors(color_series)
    # 添加数据，设置饼图的半径，是否展示成南丁格尔图
    pie1.add("222", [list(z) for z in zip(v, d)],
            radius=["15%", "100%"],
            center=["50%", "60%"],
            rosetype="area"
            )
    # 设置全局配置项
    pie1.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                        legend_opts=opts.LegendOpts(is_show=False),
                        toolbox_opts=opts.ToolboxOpts())
    # 设置系列配置项
    pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                                formatter="{b}:{c}%", font_style="italic",
                                                font_weight="bold", font_family="Microsoft YaHei"
                                                ),
                        )
    
    pie1.render(f"{rose_dir}/rose_{i}.html")
