# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 10:48:00 2017

@author: KAI
"""
import matplotlib as mlp
import numpy as np
import pymysql
import txt_mysql
import matplotlib.pyplot as plt
import Apriori
import translate_to_color
mlp.rcParams['font.family']='sans-serif'  
mlp.rcParams['font.sans-serif']=[u'SimHei']  

#rid=687423
#table_name='douyu_danmu_'+str(rid)+'_'+"25_12_2017"
rid,table_name=txt_mysql.main()
db=pymysql.connect(
        host='localhost',
        db='douyu_tv',
        user='KKKKK',
        password='123456',
        port=3306,
        charset='gbk'
        )#链接MySQL数据库
cursor=db.cursor()#数据库游标
#======总弹幕数====right====#
cursor.execute('SELECT count(*) from %s'%(table_name,))
Total_danmu_num=cursor.fetchone()[0]
print("总弹幕数:",Total_danmu_num)

#======总观众数=====right===#
cursor.execute('SELECT count(DISTINCT id) from %s'%(table_name,))
Total_pop=cursor.fetchone()[0]
print("总观众数:",Total_pop)

#==========弹幕颜色============#
cursor.execute("SELECT color,count(color) AS count from %s group by color order by count DESC"%(table_name,))
color_=cursor.fetchall()
colors={}
for i in color_:
    colors[i[0]]=i[1]
white_num=colors.pop('0')
other_num=sum(colors.values())
print('白色普通弹幕：',white_num)
print('有色弹幕',other_num)
for i in colors.items():
    print("%s,有 %d 条,占有色弹幕的 %.1f %%"%(translate_to_color.ttc(int(i[0])),i[1],i[1]/other_num*100))

#======话痨======right======#
#TOP=5
sql="SELECT nickname,id,count(id) AS count FROM %s \
group by id \
order by count DESC \
limit 5"%(table_name,)
cursor.execute(sql)
Tops=cursor.fetchall()
print("话痨榜:",Tops)

#======前五牌子比例===right=====#
sql="SELECT badge,count(DISTINCT id) AS count FROM %s \
where badge<>'NONE'\
group by badge \
order by count DESC \
limit 5"%(table_name,)
cursor.execute(sql)
Top_badges=cursor.fetchall()
labels=[];sizes=[]
for i in Top_badges:
    labels.append(i[0])
    sizes.append(i[1])
sizes=[i/sum(sizes)*100 for i in sizes]
print(Top_badges[0][0]+"的牌子数共",Top_badges[0][1])
colors='lightcoral','gold','lightskyblue','yellow','yellowgreen'
explode=0.5,0.4,0.2,0.2,0
plt.figure(1)
plt.pie(tuple(sizes), explode=explode, labels=tuple(labels), colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=50)
plt.axis('equal')
plt.title("前五牌子比例")
plt.show()
#plt.savefig('%s TOP5 badge.png'%(table_name,))

#======等级分布======right===#
sql="SELECT level FROM %s Group by id"%(table_name,)
cursor.execute(sql)
levels=cursor.fetchall()
plt.figure(2)
levels=sorted([int(j[0]) for j in levels])
lbins=np.arange(min(levels),(max(levels) if max(levels)%2==1 else max(levels)+1),1)
#levels=np.sort(levels)
plt.hist(levels,lbins,histtype='bar',facecolor='pink',alpha=0.75,rwidth=0.8)
plt.xlabel("等级区间")
plt.ylabel("出现频率") 

plt.title("观众等级分布")
plt.show()
#plt.savefig('%s Audience level.png'%(table_name,))

#====牌子等级分布====right====#
sql="SELECT blevel FROM %s"%(table_name,)+" WHERE badge = %s Group by id"
cursor.execute(sql,(labels[0],))
blevels=cursor.fetchall()
plt.figure(3)
blevels=sorted([int(j[0]) for j in blevels])
bbins=np.arange(min(blevels),(max(blevels) if max(blevels)%2==1 else max(blevels)+1),1)
plt.hist(blevels,bbins,histtype='bar',facecolor='blue',alpha=0.75,rwidth=0.8)
plt.xlabel("等级区间")
plt.ylabel("出现频率") 
plt.title("%s牌子等级分布"%(labels[0]))
plt.show()
#plt.savefig('%s badge level.png'%(table_name,))

#======自聚类======right?=====#
sql="SELECT blevel,level FROM %s"%(table_name,)+" WHERE badge = %s Group by id"
cursor.execute(sql,(labels[0],))
audience_with_badge_levels=cursor.fetchall()
audience_levels=[]
badge_levels=[]
for j in audience_with_badge_levels:
    audience_levels.append(j[0])
    badge_levels.append(j[1])
x=np.array([audience_levels,badge_levels],dtype=np.float).T
y=np.zeros(shape=(len(x),1),dtype=np.float)
for i in range(len(x)):
    y[i]=1 if x[i,0]<x[i,1] else 0
plt.figure(4)
plt.scatter(x[:,0],x[:,1],c=np.squeeze(y),s=20,cmap='RdYlBu')
X=np.linspace(min(x[:,0]),max(x[:,1]),30)
plt.plot(X,X,'k-')
plt.xlabel("牌子等级")
plt.ylabel("用户等级")
plt.show()
#plt.savefig('%s badge and level.png'%(table_name,))
'''
#======四字热词========#
MINSUPPORT=0.005 #10%的支持度
DATA=[]#数据全集
support_data={}
K=4

cursor.execute("SELECT content FROM %s"%(table_name,))
danmu=cursor.fetchall()
tmp=[]
danmu_list=[]
for j in danmu:
    for i in j:
        for k in i:
            tmp.append(k)
        danmu_list.append(tmp)
        tmp=[]
        
L, support_data = Apriori.generate_L(danmu_list, K, MINSUPPORT,support_data)#4-项集
print("Starting to create Big_Rules")
big_rules_list = Apriori.generate_big_rules(L, support_data, min_conf=1.0)
        
for Lk in L:
    print( "="*50)
    print( "frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
    print( "="*50)
    bglist={}
    for freq_set in Lk:
        bglist[freq_set]=support_data[freq_set]
    bglist=sorted(bglist.items(),key=lambda item:item[1],reverse=True)
    count=20#各取频繁项前二十
    print(bglist[0:count])
    
print()
'''
'''
print ("Big Rules")
for item in big_rules_list:
    print( item[0], "=>", item[1], "conf: ", item[2])
'''

#========语义分析=========#
'''
from sklearn.cluster import DBSCAN
sql="SELECT content FROM %s"%(table_name,)
cursor.execute(sql)
danmu_content=cursor.fetchall()
danmu_content_list=[]
for i in danmu_content:
    if i[0]:
        danmu_content_list.append(i[0])
    else:
        danmu_content_list.append(0000)
clf=DBSCAN(eps=1.5,min_samples=150)#,metric="manhattan")
#clf=KMeans(n_clusters=4)
danmu_content=np.array(danmu_content_list,dtype=np.float)
y_pred=clf.fit_predict(np.reshape(danmu_content_list,(-1,1),dtype='float'))
'''