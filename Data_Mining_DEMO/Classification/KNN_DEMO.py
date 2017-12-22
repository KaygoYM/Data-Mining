# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:07:50 2017

@author: KAI
"""

import numpy as np
from sklearn import neighbors
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt


mnist=input_data.read_data_sets("MNIST_data/", one_hot=True)
index=np.random.choice(len(mnist.test.images),50)
X_test=mnist.test.images[index]
y_test=mnist.test.labels[index]
#index=np.random.choice(len(mnist.train.images),5000)
X_train=mnist.train.images
y_train=mnist.train.labels
KNN=neighbors.KNeighborsClassifier(n_neighbors=20)
KNN.fit(X_train,y_train)
print(KNN.score(X_test,y_test))
y_pred=KNN.predict(X_test)

#A simple plotting
#The visualization of the classification of the handwriting_digits via KNN remains to be done
index=np.random.choice(len(mnist.train.images),500)
X_train=X_train[index]
y_plot_train=np.argmax(y_train[index],axis=1)
X_plot_train=np.zeros([len(X_train),2])
for i in range(len(X_train)):
    X_plot_train[i,:]=[y_plot_train[i]+np.random.rand(),0]


y_plot_pred=np.argmax(y_pred,axis=1)
X_plot_pred=np.zeros([len(X_test),2])
for i in range(len(X_test)):
    X_plot_pred[i,:]=[y_plot_pred[i]+np.random.rand(),0]


plt.scatter(X_plot_train[:,0],X_plot_train[:,1],c=y_plot_train,s=10,cmap=plt.get_cmap('RdYlBu'))
plt.scatter(X_plot_pred[:,0],X_plot_pred[:,1],c=y_plot_pred,marker="*",s=100,cmap=plt.get_cmap('RdYlBu'))
plt.colorbar()
plt.show()