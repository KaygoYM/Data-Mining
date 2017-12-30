# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 11:42:17 2017

@author: KAI
"""
import pymysql
import time
#import unicode
def main():
    db=pymysql.connect(
            host='localhost',
            db='douyu_tv',
            user='KKKKK',
            password='123456',
            port=3306,
            charset='gbk'
            )#链接MySQL数据库
    cursor=db.cursor()#数据库游标   
    if cursor:  
        print("data base has already connected")

    roomid=input('输入房间号：')
    txt = open(str(roomid)+'_'+str(time.strftime("%d_%m_%Y"))+'.txt','r',encoding='gbk')
    table_name='douyu_danmu_'+str(roomid)+'_'+str(time.strftime("%d_%m_%Y"))#create table
    sql="CREATE TABLE IF NOT EXISTS %s"%(table_name,)+"(id varchar(1024),\
    nickname varchar(1024),\
    level varchar(128),\
    content varchar(2048),\
    badge varchar(1024),\
    blevel varchar(128),\
    color varchar(128))DEFAULT CHARSET gbk"
    
    cursor.execute(sql)
    cursor.execute('delete from %s'%(table_name,))
    danmulist=[]
    for line in txt.readlines():#按行读取且处理掉换行符，效果:"\'\n'变为了''
        #line = line.encode('utf8')
        list_danmu = line.strip('\n').replace('/bl@=0','NONE').split('|')
        if len(list_danmu)!=7:#项目数
            continue
        else:
            danmulist.append(tuple(list_danmu))
        #print('line complete')
                
    try:
        insertcolumn_full="INSERT INTO %s"%(table_name,)+"(id,nickname,level,content,badge,blevel,color) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.executemany(insertcolumn_full,danmulist)#运行 

    except Exception as e:
        print(e)
    db.commit()
    return roomid,table_name
if __name__=='__main__':
    temp,temp2=main()