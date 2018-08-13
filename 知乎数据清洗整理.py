import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
% matplotlib inline


# 数据读取

data1 = pd.read_csv('C:/Users/Hjx/Desktop/知乎数据_201701.csv', engine = 'python')
data2 = pd.read_csv('C:/Users/Hjx/Desktop/六普常住人口数.csv', engine = 'python')
print(data1.head())
print(data2.head())

# 数据清洗 - 去除空值
# 文本型字段空值改为“缺失数据”，数字型字段空值改为 0 
# 要求：创建函数
# 提示：fillna方法填充缺失数据，注意inplace参数

def data_cleaning(df):
    cols = df.columns
    for col in cols:
        if df[col].dtype ==  'object':
            df[col].fillna('缺失数据', inplace = True)
        else:
            df[col].fillna(0, inplace = True)
    return(df)
# 该函数可以将任意数据内空值替换

data1_c = data_cleaning(data1)
data1_c.head(10)
# 问题1 知友全国地域分布情况，分析出TOP20
# 要求：
# ① 按照地域统计 知友数量、知友密度（知友数量/城市常住人口），不要求创建函数
# ② 知友数量，知友密度，标准化处理，取值0-100，要求创建函数
# ③ 通过多系列柱状图，做图表可视化
# 提示：
# ① 标准化计算方法 = (X - Xmin) / (Xmax - Xmin)
# ② 可自行设置图表风格

df_city = data1_c.groupby('居住地').count()  # 按照居住地统计知友数量
data2['city'] = data2['地区'].str[:-1]   # 城市信息清洗，去掉城市等级文字
#print(df_city.head())  
#print(data2.head())  

q1data = pd.merge(df_city, data2, left_index = True, right_on = 'city', how = 'inner')[['_id','city','常住人口']]
q1data['知友密度'] = q1data['_id']/q1data['常住人口'] 
#print(q1data.head())
# 统计计算知友数量，知友密度

def data_nor(df, *cols):
    colnames = []
    for col in cols:
        colname = col + '_nor'
        df[colname] = (df[col]-df[col].min())/(df[col].max()-df[col].min()) * 100
        colnames.append(colname)
    return(df,colnames)
# 创建函数，结果返回标准化取值，新列列名

resultdata = data_nor(q1data,'_id','知友密度')[0]
resultcolnames = data_nor(q1data,'_id','知友密度')[1]
q1data_top20_sl = resultdata.sort_values(resultcolnames[0], ascending=False)[['city',resultcolnames[0]]].iloc[:20]
q1data_top20_md = resultdata.sort_values(resultcolnames[1], ascending=False)[['city',resultcolnames[1]]].iloc[:20]
#print(q1data_top20_sl)
# 标准化取值后得到知友数量，知友密度的TOP20数据

fig1 = plt.figure(num=1,figsize=(12,4))
y1 = q1data_top20_sl[resultcolnames[0]]
plt.bar(range(20),
        y1,
        width = 0.8,
        facecolor = 'yellowgreen',
        edgecolor = 'k',
        tick_label = q1data_top20_sl['city'])
plt.title('知友数量TOP20\n')
plt.grid(True, linestyle = "--",color = "gray", linewidth = "0.5", axis = 'y')  
for i,j in zip(range(20),y1):
    plt.text(i+0.1,2,'%.1f' % j, color = 'k',fontsize = 9)

fig2 = plt.figure(num=2,figsize=(12,4))
y2 = q1data_top20_sl[resultcolnames[0]]
plt.bar(range(20),
        y2,
        width = 0.8,
        facecolor = 'lightskyblue',
        edgecolor = 'k',
        tick_label = q1data_top20_md['city'])
plt.grid(True, linestyle = "--",color = "gray", linewidth = "0.5", axis = 'y')  
plt.title('知友密度TOP20\n')
for i,j in zip(range(20),y2):
    plt.text(i+0.1,2,'%.1f' % j, color = 'k',fontsize = 9)
# 创建图表
