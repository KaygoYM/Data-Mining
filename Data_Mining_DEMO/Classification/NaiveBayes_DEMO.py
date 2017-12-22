# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:24:21 2017

@author: KAI
"""

from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation



iris = datasets.load_iris()
#X = iris.data[:, [0, 2]]
X = iris.data
y = iris.target

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

NaiveBayes = GaussianNB().fit(X_train, y_train)  
y_pred=NaiveBayes.predict(X_test)

count=0;
for i in range(len(y_pred)):
    if y_pred[i]!=y_test[i]:
        count+=1
        print("The"+str(i)+"th prediction is "+str(y_pred[i])+",but the reality is "+str(y_test[i]))
accu=1-count/len(y_pred)
print("The accuracy of prediction is "+str(accu))