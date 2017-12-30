# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:42:04 2017

@author: KAI
REF:CSDN Blog
"""


#coding=utf-8
#爬取斗鱼颜值妹子图片
import json
import urllib.request 
import time
from bs4 import BeautifulSoup
#定义为方法
def getHTML(chaper_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    #伪装headers
    req = urllib.request.Request(url=chaper_url, headers=headers)  
    page=urllib.request.urlopen(req)  
    html=page.read()
    return html

#开始根据链接爬图片保存数据
def getImage(html):
    #根据API返回的是json格式数据
    yz_info=json.loads(html)['data']
    for i in yz_info:
        url = i['room_src']
        name=i['nickname']
        rid=i['room_id']
        print('开始下载:%s'%(name,))
        try:
            urllib.request.urlretrieve(url,'D:/Workspace/Data_Mining/Data_Mining_App/Douyu_Beauty/beauty_pic/%s.jpg'%(name+'_'+str(rid),))
            print(url)
        except Exception as e:
            print(e)
            print('出现异常,地址为：%s'%url)
        finally:
            time.sleep(0.5)
if __name__=='__main__':
    fileimg = getHTML('http://open.douyucdn.cn/api/RoomApi/live/yz')
    getImage(fileimg)

#douyu_API
