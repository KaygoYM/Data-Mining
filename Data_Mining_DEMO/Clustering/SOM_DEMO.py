# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:56:14 2017

@author: KAI
"""
import numpy as np
from sklearn import preprocessing
from sklearn.datasets.samples_generator import make_blobs
from sklearn import cross_validation
import matplotlib.pyplot as plt
#初始化输入层与竞争层神经元的连接权值矩阵
def initCompetition(n,m,d):
    #随机产生0-1之间的数作为权值
    com_weight = np.random.normal(0,1,[n,m*d])#n输入，m*d个竞争神经元
    com_weight = preprocessing.minmax_scale(com_weight.T,feature_range=(-1,1))
    com_weight = np.reshape(com_weight,(n,m,d))
    return com_weight

#得到获胜神经元的索引值
def getWinner(X,W):
    MAX=-9999
    n,m,d=W.shape
    
    for i,j in zip(range(m),range(d)):
        temp=np.dot(W[:,i,j],X)
        if (temp>MAX):
            MAX=temp
            w=W[:,i,j]
            max_i=i
            max_j=j
    return w,max_i,max_j
#得到神经元的N邻域
def getNeibor(n , m , N_neibor , com_weight):
    res = []
    _,mm,dd= com_weight.shape
    for i,j in zip(range(mm),range(dd)):
        N = int(((i-n)**2+(j-m)**2)**0.5)
        if N<=N_neibor:
            res.append((i,j,N))
    return np.array(res)
#学习率函数
def eta(t,N):
    return (0.3/(t+1))*(np.exp(-N))

#SOM算法的实现
def SOM_train(W,X_train,time):
    N_initial=round(0.8*max(W.shape[1],W.shape[2]))
    for X in X_train:
        W_winner,i_win,j_win=getWinner(X,W)
        Nt=getNeibor(i_win,j_win,N_initial,W)#N为半径
        index,rad=np.array_split(Nt,2,axis=1)
        
    #开始调整权值
        for i,j in zip(index[:,0],index[:,1]):
            w=W[:,i,j]
            if eta(time,N_initial)>1e-6:
                w=w+eta(time,N_initial)*(X-w)
            else:
                return W
        N_initial=0.3/(time+1)
    return W
    
def SOM_draw(W,X_data):
    key=[]
    for X in X_data:
         _,i,j=getWinner(X,W)
         key.append(i*W.shape[1]+j)
    return key
         
         
if __name__=='__main__':

    X,y=make_blobs(n_samples=100,n_features=2,centers=3)#n_redundant=0,
                        #n_informative=2,n_clusters_per_class=1,n_classes=3,scale=100)
    X=preprocessing.minmax_scale(X,feature_range=(-1,1))
    MAX_NR=1000

    X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)
    W=initCompetition(X_train.shape[1],6,6)
    for time in range(MAX_NR):
        W=SOM_train(W,X_train,time)
    K_train=SOM_draw(W,X_train)
    K_test=SOM_draw(W,X_test)
    plt.subplot(221)
    plt.scatter(X_train[:,0],X_train[:,1],c=y_train)
    plt.subplot(222)
    plt.scatter(X_train[:,0],X_train[:,1],c=K_train)
    plt.subplot(223)
    plt.scatter(X_test[:,0],X_test[:,1],c=y_test)
    plt.subplot(224)
    plt.scatter(X_test[:,0],X_test[:,1],c=K_test)