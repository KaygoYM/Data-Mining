# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 19:48:46 2018

@author: KAI
"""


from pyspark import SparkContext
from pyspark import SparkConf
import pyspark.mllib.recommendation as rd
import numpy as np

conf = SparkConf().setMaster("local[*]").setAppName("MyApp")
sc = SparkContext(conf=conf)#local本地URL #APPname
#===============================================用户推荐====================================#
#===============================================用户推荐====================================#
print('='*25+'用户推荐'+'='*25)
raw_rating_data=sc.textFile("./ml-100k/u.data")
rating_data=raw_rating_data.map(lambda line:line.split('\t')[:3])#list
print(rating_data.take(5))

# 由于ALS模型需要由Rating记录构成的RDD作为参数，因此这里用rd.Rating方法封装数据
ratings = rating_data.map(lambda k: rd.Rating(int(k[0]), int(k[1]), float(k[2])))
'''
lambda表达式以元组作为参数，在python2和python3中写法是有区别的：
# python2
lambda (x, w) : x * w
#python3
lambda x_w : x_w[0] * x_w[1]
'''
print(ratings.first())
#Rating(user=196, product=242, rating=3.0)
#print(RAWratings.take(3))
model = rd.ALS.train(ratings, 50, 10, 0.01)
#model.userFeatures

# 利用该模型预测789用户对123电影的评分
predictedRating = model.predict(789, 123)
print(predictedRating)

topKRecs=model.recommendProducts(789,10)
print(topKRecs)


#==========检验=============#
movies = sc.textFile('./ml-100k/u.item')
#movies.first()
#u’1|Toy Story (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0’

movies_fields = movies.map(lambda line: line.split('|'))
title_data = movies_fields.map(lambda fields: (int(fields[0]), fields[1])).collect()
titles = dict(title_data)
print(titles[123])

# keyBy从ratings RDD创建一个键值对RDD，选取user为主键
# lookup返回给定键的数据
moviesForUser = ratings.keyBy(lambda rating: rating.user).lookup(789) # 返回的是list
print("moviesForUser(size):",len(moviesForUser))#list长度
#print(moviesForUser[0:10])

# sorted(list, key=lambda..., reverse=True)是对list的排序函数
# sc.parallelize(data)并行化数据，转换为rdd后才能用map方法
moviesForUser = sorted(moviesForUser, key=lambda r: r.rating, reverse=True)[0:10] # 结果为789对他看过的电影给出的评分Top10
User_rating_Top10=[(titles[r.product], r.rating) for r in moviesForUser]
print(User_rating_Top10)
Recom_Top10=[(titles[r.product], r.rating) for r in topKRecs]
print(Recom_Top10)

#===============================================物品推荐====================================#
#===============================================物品推荐====================================#
print('='*25+'物品推荐'+'='*25)
itemId = 567
itemVec = model.productFeatures().lookup(itemId)[0]
from scipy.spatial.distance import cosine
# cosine函数实际上是是求1-cosine,便于我们后面的排序，对1-cosine从小到大排等价于对cosine从大到小排
sims = model.productFeatures().map(lambda k: (k[0], cosine(k[1], itemVec)))
print(sims.first())
sortedSims = sims.sortBy(lambda s: s[1]).take(10)#最相似的前十个物品
print(sortedSims)
#[(567, 0.0), (563, 0.24824939014928582), (436, 0.26345700050207055), (670, 0.27669948452712556), 
#(230, 0.28365450647789237), (109, 0.28618185250983319), (208, 0.29951515961600639), (642, 0.29994930626905392), 
#(405, 0.30848232528755659), (1263, 0.30936115523097651)]
#找到title打印出来
print(titles[itemId])
Sims_Top10=[(titles[id], sim) for (id, sim) in sortedSims]
print(Sims_Top10)

#==============================================模型效果评价=================================#
#==============================================模型效果评价=================================#
#~~~~~~~~~~~~一条数据的MSE
print('='*25+'模型效果评价'+'='*25)
actualRating = moviesForUser[0]
predictedRating = model.predict(789, actualRating.product)
squaredError = (actualRating.rating - predictedRating) ** 2
print("实际评分: %f, 预测评分: %f, 方差: %f. " % (actualRating.rating, predictedRating, squaredError))

usersProducts = ratings.map(lambda r: (r.user, r.product))
# predictAll方法以对(int, int)形式的rdd作为参数，这点与scala不同，scala直接用predict
predictions = model.predictAll(usersProducts).map(lambda r: ((r.user, r.product), r.rating))
print("Predictions:TAKE 5",predictions.take(5))
ratingsAndPredictions = ratings.map(lambda r: ((r.user, r.product), r.rating)).join(predictions)
print("Ratings and Predictions:",ratingsAndPredictions.take(5))
#~~~~~~~~~~~整体MSE
MSE = ratingsAndPredictions.map(lambda k: (k[1][0]- k[1][1]) ** 2).sum()/ratingsAndPredictions.count()
print("Mean Squared Error =", MSE)
#K值平均率
# 计算APK(Average Precision at K metric)K值平均准确率
def avgPrecisionK(actual, predicted, k):
    predK = predicted[0:k]
    score = 0.0
    numHits = 0.0
    for i, p in enumerate(predK):
        if(p in actual):
            numHits += 1
            score += numHits / float(i + 1)
    if(len(actual) == 0):
        return 1.0
    else:
        return score / float(min(len(actual), k))
#~~~~~~~~~~~~~~~一条K值平均率
actualMovies = [mu.product for mu in moviesForUser]
print(actualMovies)
#[127, 475, 9, 50, 150, 276, 129, 100, 741, 1012]

predictedMovies = [tkr.product for tkr in topKRecs]
print(predictedMovies)
#[708, 482, 502, 603, 23, 182, 484, 479, 1020, 494]
apk10 = avgPrecisionK(actualMovies, predictedMovies, 10)
print(apk10)
#~~~~~~~~~~~~~~所有的整体K值平均率
itemFactors = model.productFeatures().map(lambda k:k[1]).collect()
itemMatrix = np.array(itemFactors)
#物品矢量
print(itemMatrix)
print(itemMatrix.shape)
#(1682, 50)
#(电影数目，因子维数)
imBroadcast = sc.broadcast(itemMatrix)
from array import array
scoresForUser = model.userFeatures().map(lambda k: (k[0], np.dot(imBroadcast.value, k[1])))
allRecs = scoresForUser.map(lambda k:(k[0], sorted(zip(np.arange(1, k[1].size), k[1]), key=lambda x: x[1], reverse=True))
                           ).map(lambda k: (k[0], np.array(k[1], dtype=int)[:,0]))
#计算每个用户的推荐
print(allRecs.first()[0])
print(allRecs.first()[1])
#以上为所有推荐电影ID（按评级排序）

# groupByKey返回(int, ResultIterable), 其中ResultIterable.data才是数据
userMovies = ratings.map(lambda r: (r.user, r.product)).groupByKey()
print(userMovies.first()[0])
print(userMovies.first()[1].data)
#以上为所有实际电影ID
#将userMovies和allRecs送入K平均率.join()
K = 10
MAPK = allRecs.join(userMovies).map(lambda k:avgPrecisionK(k[1][1].data, k[1][0], K)
                                   ).sum() / allRecs.count()
print("Mean Average Precision at K =", MAPK)

#==============================================MLLIB内置函数=================================#
#===============================================MLLIB内置函数================================#
print('='*25+'MLLIB内置函数效果'+'='*25)
from pyspark.mllib.evaluation import RegressionMetrics
predictedAndTrue = ratingsAndPredictions.map(lambda p:(p[1][0],p[1][1]))
regressionMetrics = RegressionMetrics(predictedAndTrue)
print("Mean Squared Error =", regressionMetrics.meanSquaredError)
print ("Root Mean Squared Error =", regressionMetrics.rootMeanSquaredError)

# 使用MLlib内置的评估函数计算MAP, 它取所有物品来计算，不是取前K个，因此不用设定K值,故不叫MAPK
from pyspark.mllib.evaluation import RankingMetrics
predictedAndTrueForRanking = allRecs.join(userMovies).map(lambda k:
                                                        (k[1][0], array(k[1][1].data)))
print(predictedAndTrueForRanking.first())
rankingMetrics = RankingMetrics(predictedAndTrueForRanking)
print( "Mean Average Precision =", rankingMetrics.meanAveragePrecision)
# 用我们自己实现的方法来计算MAPK，当K值较大时，结果同上面一样
K = 2000
MAPK2000 = allRecs.join(userMovies).map(lambda k:avgPrecisionK(k[1][1].data, k[1][0], K)
                                   ).sum() / allRecs.count()
print("Mean Average Precision at 2000 =", MAPK2000)

