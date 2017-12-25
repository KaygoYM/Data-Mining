# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 10:48:00 2017

@author: KAI
"""
import re
import pymysql
import time
import txt_mysql
import matplotlib.pyplot as plt

rid=687423
table_name='douyu_danmu_'+str(rid)+'_'+str(time.strftime("%d_%m_%Y"))
#rid,table_name=txt_mysql.main()
db=pymysql.connect(
        host='localhost',
        db='douyu_tv',
        user='KKKKK',
        password='123456',
        port=3306,
        charset='gbk'
        )#链接MySQL数据库
cursor=db.cursor()#数据库游标
#======总弹幕数========#
cursor.execute('SELECT count(*) from %s'%(table_name,))
Total_danmu_num=cursor.fetchone()[0]
#======总观众数========#
cursor.execute('SELECT count(DISTINCT id) from %s'%(table_name,))
Total_pop=cursor.fetchone()[0]
#======话痨============#
#TOP=5
sql="SELECT nickname,count(*) AS count FROM %s \
group by id \
order by count DESC \
limit 5"%(table_name,)
cursor.execute(sql)
Tops=cursor.fetchall()
#======前五牌子比例========#
sql="SELECT badge,count(*) AS count FROM %s \
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
colors='lightcoral','gold','lightskyblue','purple','yellowgreen'
explode=0.5,0.4,0.2,0.2,0
plt.figure(1)
plt.pie(tuple(sizes), explode=explode, labels=tuple(labels), colors=colors, autopct='%1.1f%%', shadow=False, startangle=50)
plt.axis('equal')
plt.show()
#======等级分布=========#
sql="SELECT level FROM %s group by id"%(table_name,)
cursor.execute(sql)
levels=cursor.fetchall()