# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:05:59 2017
Apriori + MySQL
@author: KAI
"""

import pymysql
#import itertools
import Apriori 

MINSUPPORT=0.05 #5%的支持度
DATA=[]#数据全集
L1=set()
support_data={}
#all_doubleitem=set()
K=3#最多做到3-项集

#open local database connection
db=pymysql.connect(
        host='localhost',
        db='system_key',
        user='KKKKK',
        password='123456',
        port=3306,
        charset='utf8'
        )#链接MySQL数据库
cursor=db.cursor()#数据库游标
cursor.execute("SELECT project_id,group_concat(tag_name) from sys_keywords group by project_id;")
data_set_all=cursor.fetchall()#指针对象的cursor.fetchall()可取出指针结果集中的所有行，返回的结果集一个元组(tuples)。
cursor.execute("SElECT count(DISTINCT project_id) FROM sys_keywords;")#表名：sys_keywords
baskets=cursor.fetchone()[0]#篮子数
#指针对象的cursor.fetchone()从查询结果集中返回下一行。
for i in range(baskets):
    DATA.append(data_set_all[i][1].split(","))#产生data_base_set C1
#support_data 字典- k-项集支持度
#L1 
cursor.execute("SELECT DISTINCT tag_name \
               FROM sys_keywords \
               GROUP BY 1\
               HAVING COUNT(project_id)>=%s ORDER BY tag_name",
               (MINSUPPORT*baskets))
L1_pre=cursor.fetchall()
for i in range(len(L1_pre)):
    L1.add(frozenset({L1_pre[i][0]}))
    cursor.execute("SELECT count(project_id) FROM sys_keywords WHERE tag_name=%s",(L1_pre[i][0]))
    support_data[frozenset({L1_pre[i][0]})]=cursor.fetchone()[0]/baskets
print("L1 is created")
#开始主循环部分
L, support_data = Apriori.generate_L(DATA, K, MINSUPPORT,L1,support_data)#3-项集
print("Starting to create Big_Rules")
big_rules_list = Apriori.generate_big_rules(L, support_data, min_conf=0.7)
print()
for Lk in L:
    print( "="*50)
    print( "frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
    print( "="*50)
    for freq_set in Lk:
        print (freq_set, support_data[freq_set])
print()
print ("Big Rules")
for item in big_rules_list:
    print( item[0], "=>", item[1], "conf: ", item[2])
