# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:22:17 2017

@author: KAI
"""

from sklearn.cluster import DBSCAN,KMeans
from sklearn.datasets import make_blobs
from sklearn import preprocessing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  

X,y=make_blobs(n_samples=1000,n_features=3,centers=4)
X=preprocessing.minmax_scale(X)

clf=DBSCAN(eps=0.1,min_samples=20,metric="euclidean")
y_pred=clf.fit_predict(X)

y_pred_km=KMeans(n_clusters=4).fit_predict(X)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("DBSCAN")
ax.scatter(X[:,0],X[:,1],X[:,2],c=y_pred,s=20,cmap='RdYlBu')

fig2=plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.set_title("KMeans")
ax2.scatter(X[:,0],X[:,1],X[:,2],c=y_pred_km,s=20,cmap='RdYlBu')
plt.show()