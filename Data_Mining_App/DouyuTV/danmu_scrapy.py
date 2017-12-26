# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:59:18 2017

@author: KAI
"""

# 这个抓取弹幕,然后把用户的id，昵称，等级，弹幕内容都保存到mongodb中
import multiprocessing
import re
import socket
import time

#import pymysql
import requests
from bs4 import BeautifulSoup
#import numpy as np
#import pandas as pd  


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))
#setsockopt(client,SOL_SOCKET,SO_KEEPALIVE,true)
'''
danmu_path = re.compile(b'txt@=(.+?)/cid@')
uid_path = re.compile(b'uid@=(.+?)/nn@')
nickname_path = re.compile(b'nn@=(.+?)/txt@')
level_path = re.compile(b'level@=([1-9][0-9]?)/sahf')
badgename_path = re.compile(b'bnn@=(.+?)/bl@')
'''
danmu_path = re.compile(b'txt@=(.+?)/')
uid_path = re.compile(b'uid@=(.+?)/')
nickname_path = re.compile(b'nn@=(.+?)/')
level_path = re.compile(b'level@=([1-9][0-9]?)/')
badgename_path = re.compile(b'bnn@=(.+?)/')
badgelevel_path=re.compile(b'bl@=(.+?)/')

def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def starting(roomid):
    print('---------------欢迎连接到{}的直播间---------------'.format(get_name(roomid)))
    msg = 'type@=loginreq/username@=rieuse/password@=douyu/roomid@={}/\0'.format(roomid)
    sendmsg(msg)
    #print(client.recv(1024))
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    sendmsg(msg_more)
    print("Succeed logging in")
    while True:
        data = client.recv(2048)#bytes-like-objects
        uid_more = uid_path.findall(data)
        nickname_more = nickname_path.findall(data)
        level_more = level_path.findall(data)
        danmu_more = danmu_path.findall(data)
        badgename_more=badgename_path.findall(data)
        badgelevel_more=badgelevel_path.findall(data)
        #print(data)
        if not level_more:
            level_more = b'0'
        if not data:
            print("NOT DATA")
            print(data)
            break
            #continue
        else:
            for i in range(0, len(danmu_more)):
                try:
                    product={'uid':uid_more[i].decode(errors='ignore'),
                             'nickname':nickname_more[i].decode(errors='ignore'),
                             'level':level_more[i].decode(errors='ignore'),
                             'danmu':danmu_more[i].decode(errors='ignore'),
                             'badge':badgename_more[i].decode(errors='ignore'),
                             'blevel':badgelevel_more[i].decode(errors='ignore')
                             }
                    lines=[uid_more[i].decode(errors='ignore')+'|',
                           nickname_more[i].decode(errors='ignore')+'|',
                           level_more[i].decode(errors='ignore')+'|',
                           danmu_more[i].decode(errors='ignore')+'|',
                           badgename_more[i].decode(errors='ignore')+'|',
                           badgelevel_more[i].decode(errors='ignore')]
                    '''
                    product={'uid':uid_more[i].decode(),
                             'nickname':nickname_more[i].decode(),
                             'level':level_more[i].decode(),
                             'danmu':danmu_more[i].decode(),
                             'badge':badgename_more[i].decode()
                             }
                    lines=[uid_more[i].decode()+' ',
                           nickname_more[i].decode()+' ',
                           level_more[i].decode()+' ',
                           danmu_more[i].decode()+' ',
                           badgename_more[i].decode()]
                    '''
                    my_file=open(str(roomid)+'.txt','a+')
                    my_file.writelines(lines)
                    my_file.write('\n')
                    my_file.close()
                    print(product)
                    
                    
                except Exception as e:
                    print(e)
                    continue
    #client.close()
    print("成功写入TXT")


def keeplive():
    while True:
        #msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        msg='type@=mrkl/'
        sendmsg(msg)
        print("init_live")
        time.sleep(10)


def get_name(roomid):
    r = requests.get("http://www.douyu.com/" + roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'zb-name'}).string


if __name__ == '__main__':
    room_id = input('请出入房间ID： ')
    p2 = multiprocessing.Process(target=keeplive)
    p2.start()
    while True:
        p1 = multiprocessing.Process(target=starting, args=(room_id,))
        p1.start()
        p1.join()
        print("p1:",p1.is_alive())
