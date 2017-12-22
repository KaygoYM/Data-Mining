# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:50:41 2017

@author: KAI
"""
"""
Load and return the iris dataset (classification).
The iris dataset is a classic and very easy multi-class classification dataset.
Classes	3
Samples per class	50
Samples total	150
Dimensionality	4
Features	real, positive
"""
"""
150	4	setosa	versicolor	virginica
5.1	3.5	1.4	0.2	0

"""
#import numpy as np
#import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier



# 仍然使用自带的iris数据
iris = datasets.load_iris()
#X = iris.data[:, [0, 2]]
X = iris.data
y = iris.target

# 训练模型，限制树的最大深度4[]
cart = DecisionTreeClassifier()
#拟合模型
cart.fit(X, y)


# 画图
"""
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))

Z = cart.predict(np.c_[xx.ravel(), yy.ravel()])#拉直==多维变一维
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
plt.show()
"""
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(cart, out_file=f,
                             feature_names=iris.feature_names,
                             class_names=iris.target_names,
                             filled=True,special_characters=True,rounded=True)
#print in command:
#dot -Tpdf iris.dot -o iris.pdf