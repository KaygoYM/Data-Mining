# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 20:41:38 2017

@author: KAI
"""

from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans,MiniBatchKMeans
import matplotlib.pyplot as plt

X,y=make_blobs(n_samples=1000,n_features=2,centers=4)#n_redundant=0,
                        #n_informative=2,n_clusters_per_class=1,n_classes=3,scale=100)
X=preprocessing.minmax_scale(X,feature_range=(-1,1))
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

clf=KMeans(n_clusters=4)
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)

clf_mini=MiniBatchKMeans(n_clusters=4,batch_size=25)
clf_mini.fit(X_train,y_train)
y_min_pred=clf_mini.predict(X_test)

ax1=plt.subplot(3,1,1)
ax1.scatter(X_test[:,0],X_test[:,1],c=y_pred)
centroids = clf.cluster_centers_ #获取聚类中心
ax1.scatter(centroids[:,0],centroids[:,1],c='red',marker='*')
ax1.set_title("(Normal) Kmeans")

ax2=plt.subplot(3,1,2)
ax2.scatter(X_test[:,0],X_test[:,1],c=y_min_pred)
centroids_min = clf_mini.cluster_centers_ #获取聚类中心
ax2.scatter(centroids_min[:,0],centroids_min[:,1],c='red',marker='>')
ax2.set_title("(Mini) Kmeans")

ax3=plt.subplot(3,1,3)
ax3.scatter(X_test[:,0],X_test[:,1],c=y_test)
ax3.set_title("Real data")
inertia = clf.inertia_ # 获取聚类准则的总和
inertia_min=clf_mini.inertia_
plt.show