# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 11:59:13 2018

@author: KAI
"""

from pyspark import SparkContext
from pyspark import SparkConf
import matplotlib.pyplot as plt
import numpy as np

conf = SparkConf().setMaster("local[*]").setAppName("MyApp")
sc = SparkContext(conf=conf)#local本地URL #APPname
#==============用户信息===============#
user_data=sc.textFile('./ml-100k/u.user',use_unicode=True)
print(user_data.first())

user_fields=user_data.map(lambda line:line.split('|'))
num_users=user_fields.map(lambda fields:fields[0]).count()
num_genders=user_fields.map(lambda fields:fields[2]).distinct().count()
num_occupations=user_fields.map(lambda fields:fields[3]).distinct().count()
num_zipcodes=user_fields.map(lambda fields:fields[4]).distinct().count()
print("Users: %d ,Genders: %d, Occupations: %d, ZIP codes: %d"%(num_users,num_genders,num_occupations,num_zipcodes))

#~~~~~年龄分布~~~~#
ages=user_fields.map(lambda x :int(x[1])).collect()
plt.figure(1)
plt.hist(ages,bins=20,color='gold',histtype='bar',rwidth=0.8,stacked=True)
#~~~~~职业分布~~~~#
count_by_occupation=user_fields.map(lambda fields:(fields[3],1)).reduceByKey(lambda x,y:x+y).collect()
#[('other', 105), ('executive', 32), ('administrator', 79), ('student', 196), ('educator', 95), ('programmer', 66), 
#('homemaker', 7), ('artist', 28), ('engineer', 67), ('none', 9), ('retired', 14), ('doctor', 7), ('technician', 27), 
#('writer', 45), ('lawyer', 12), ('scientist', 31), ('entertainment', 18), ('librarian', 51), ('marketing', 26), 
#('healthcare', 16), ('salesman', 12)]
#print(count_by_occupation)
x_axis1=np.array([c[0] for c in count_by_occupation])
y_axis1=np.array([c[1] for c in count_by_occupation])
x_axis=x_axis1[np.argsort(y_axis1)]
y_axis=y_axis1[np.argsort(y_axis1)]
pos=np.arange(len(x_axis))
width=1.0
plt.figure(2)
ax=plt.axes()
ax.set_xticks(pos+(width/2))
ax.set_xticklabels(x_axis)

plt.bar(pos,y_axis,width,color='purple',edgecolor='black')
plt.xticks(rotation=30)
#==============电影信息================#
movie_data=sc.textFile('./ml-100k/u.item')
print(movie_data.first())
print('Movies: ',movie_data.count())
def convert_year(x):
    try:
        return int(x[-4:])
    except:
        return 1900
def extract_title(raw):
    import re
    grps=re.search("\((\w+)\)",raw)#括号间非单词(数字)
    #匹配为电影年份(1995)
    #print("raw,",raw)
    #print("grps,",grps)
    if grps:
        return raw[:grps.start()].strip()#只选取标题部分，并删除末尾空白
    else:
        return raw
movie_fields=movie_data.map(lambda lines:lines.split('|'))
years=movie_fields.map(lambda fields:fields[2]).map(lambda x:convert_year(x))
years_filtered=years.filter(lambda x :x!=1900)
movie_ages_=years_filtered.map(lambda yr:1998-yr).countByValue()#电影年龄的统计计数
#defaultdict(<class 'int'>, {3: 219, 2: 355, 4: 214, 31: 5, 21:: 5, 16: 13, 8: 24, 6: 37, 7: 22, 61: 4, 4, 5: 126, 
#33: 5, 16: 13, 8: 24, 6: 37, 7: 22, 61: 4, 1: 286, 17: 12, 28: 3, 26: 3, 
#37: 3, 59: 7, 57: 5, 30: 6, 29: 4, 44: 7, 27: 7, 10: 11, 25: 4, 19: 9, 
#11: 13, 12: 15, 9: 15, 24: 8, 18: 8, 13: 7, 32: 2, 41: 8, 38: 5, 14: 8, 
#15: 5, 23: 6, 0: 65, 58:7: 5, 36: 5, 65: 2, 42: 4, 35: 6,
#40: 9, 53: 4, 22: 5, 20: 4, 39: 4, 56: 2, 45: 2, 52: 5, 43: 5, 60: 3, 64: 4,
#49: 4, 50: 3, 55: 4, 54: 5, 62: 2, 63: 4, 68: 1, 46: 3, 67: 1, 76: 1, 51: 5, 66: 1, 72: 1})
#print(movie_ages)
movie_ages= sorted(movie_ages_.items(), key=lambda d:d[0], reverse = False)
#print(tuple(movie_ages))
values=[];bins=[]
for i in movie_ages:
    values.append(i[1])
    bins.append(i[0])
plt.figure(3)
plt.hist(values,bins=bins,color='red',edgecolor='black',normed=True)
#
raw_titles=movie_fields.map(lambda k:k[1])
for item in raw_titles.take(10):
    print(extract_title(item))
    

#==============评级信息===================#
ratings_data=sc.textFile("./ml-100k/u.data")
print(ratings_data.first())
print("Ratings: ",ratings_data.count())
#user id | item id | rating | timestamp. 
rating_data=ratings_data.map(lambda line:line.split('\t'))#list
ratings=rating_data.map(lambda fields:int(fields[2]))#所有的评分
max_rate=ratings.reduce(lambda x,y:max(x,y))#两两依次传入
min_rate=ratings.reduce(lambda x,y:min(x,y))
mean_rate=ratings.sum()/ratings.count()
median_rate=np.median(ratings.collect())
rate_per_user=ratings.count()/num_users
rate_per_movie=ratings.count()/movie_data.count()
print("MIN: %d,MAX: %d,AVG: %2.2f,Median: %d,AVG_rate_per_user: %2.2f,AVG_rate_per_movie: %2.2f"%(min_rate,max_rate,mean_rate,median_rate,
                                                                                                  rate_per_user,rate_per_movie))
print(ratings.stats())
plt.figure(4)
count_by_rating=ratings.countByValue()
x_axis=np.array(list(count_by_rating.keys()))
y_axis1=[float(c) for c in count_by_rating.values()]
y_axis=np.array(y_axis1)/sum(y_axis1)#归一化
ax=plt.axes()
print(x_axis)
pos=np.arange(len(x_axis))
ax.set_xticks(pos+(width/2))
ax.set_xticklabels(x_axis)
plt.bar(x_axis,y_axis,width,color='pink',edgecolor='black')
plt.xticks(rotation=30)#刻度转30度

#========各用户评级次数分布=============#
user_group_ratings=rating_data.map(lambda fields:(int(fields[0]),int(fields[2])))
user_group_rating=user_group_ratings.groupByKey()#tuple
#print(len(user_group_rating.first()[1]))

user_ratings_byuser = user_group_rating.map(lambda k: (k[0],len(k[1])))
all_rating_u=user_ratings_byuser.map(lambda k :k[1]).collect()#所有计数的数值
plt.figure(5)
plt.hist(all_rating_u,bins=200,color='lightblue',edgecolor='black',normed=True)

plt.show()