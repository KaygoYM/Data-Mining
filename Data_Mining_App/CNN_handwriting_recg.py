# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:12:14 2017

@author: hamch
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt

mnist=input_data.read_data_sets('MNIST_data',one_hot=True)
print(mnist.train.images.shape)
print(mnist.train.labels.shape)

#examples_to_show=20
BATCH_SIZE=200

x_test=mnist.test.images[:200]
y_test=mnist.test.labels[:200]

tf_x=tf.placeholder(tf.float32,[None,28*28])
image=tf.reshape(tf_x,[-1,28,28,1])#(batch height,width,channel)
# CNN needs tensor to input
tf_y=tf.placeholder(tf.float32,[None,10])

#Neural Network
#l1=tf.layers.dense(tf_x,100,tf.nn.relu)
#output=tf.layers.dense(l1,10)

#CNN
cnn1=tf.layers.conv2d(
        inputs=image,
        filters=16, #shape(28,28,16)
        kernel_size=5,
        strides=1,
        padding='same',
        activation=tf.nn.relu)
pool1=tf.layers.max_pooling2d(
        cnn1,
        pool_size=2,
        strides=2)#->shape(14,14,16)
cnn2=tf.layers.conv2d(pool1,32,5,1,'same',activation=tf.nn.relu)#(14,14,32)
pool2=tf.layers.max_pooling2d(cnn2,2,2)#(7,7,32)

output=tf.layers.dense(tf.reshape(pool2,[-1,7*7*32]),10)


loss=tf.losses.mean_squared_error(tf_y,output)
optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.5)
train_op=optimizer.minimize(loss)
accuracy=tf.metrics.accuracy(labels=tf.argmax(tf_y,axis=1),predictions=tf.argmax(output,axis=1),)[1]
#start training
sess=tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())

for step in range(600):
    xs,ys=mnist.train.next_batch(BATCH_SIZE)
    k,r_loss,pred,acc=sess.run([train_op,loss,output,accuracy],feed_dict={tf_x:xs,tf_y:ys})
    if step % 50==0:
       print("loss=%.4f,accuracy=%.4f" %(r_loss,acc))
      
#test result
examples_to_show=20
test_output=sess.run(output,feed_dict={tf_x:x_test[:examples_to_show][:]})
pred_y=np.argmax(test_output,axis=1)
print(pred_y,'prediction number')
print(np.argmax(y_test[:examples_to_show][:],axis=1),'real number')

f, a = plt.subplots(2, examples_to_show, figsize=(examples_to_show, 2))
for i in range(examples_to_show):
    a[0][i].imshow(np.reshape(x_test[i][:], (28, 28)))
    a[1][i].text(0.5,0,str(pred_y[i]))
plt.show()
