# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:37:31 2017

@author: KAI
"""
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.datasets.samples_generator import make_classification
from sklearn.svm import SVC
import matplotlib.pyplot as plt

X,y=make_classification(n_samples=600,n_features=2,n_redundant=0,
                        n_informative=2,n_clusters_per_class=1,n_classes=3,scale=100)
X=preprocessing.minmax_scale(X,feature_range=(-1,1))
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

clf=SVC()
clf.fit(X_train,y_train)
print(clf.score(X_test,y_test))
y_pred=clf.predict(X_test)
plt.scatter(X_test[:,0],X_test[:,1],c=y_pred)