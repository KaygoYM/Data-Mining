# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 15:30:46 2017

@author: KAI
"""
import numpy as np
import networkx as nx 

def graph_matrix(A):
    for i in range(len(A)):
        if((A[i]==0).all()):
            pass
        else:
            A[i]=A[i]/sum(A[i])
    return A

def PageRank(PR_init,A,eta,q):
    #q:阻尼系数
    while(1):
        R=(1-q)*np.ones_like(PR_init)+q*np.matmul(A.T,PR_init)
        if (np.linalg.norm(R-PR_init)<eta):
            return R
        else:
            PR_init=R         

if __name__=='__main__':
    A=np.array([[0,1,1,0,0,0],
                [1,0,1,0,0,0],
                [0,1,0,0,0,0],
                [0,0,1,0,1,1],
                [0,0,0,0,0,0],
                [0,0,0,1,1,0]],dtype=float)
    A=graph_matrix(A)
    PR0=np.ones((len(A),1))
    PR_fin=PageRank(PR0,A,1e-8,0.85)
    graph = nx.from_numpy_matrix(A,create_using=nx.DiGraph())
    nx.draw(graph,arrows=True,with_labels=True)