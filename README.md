# 课程设计

## 1 KNN max value 0.48
## 2 决策树 max value 0.615    when the step is 302 the accurary is the highest , 0.615
## 3 朴素贝叶斯 max value 0.612
## 4 RNN max value 0.972   
## 5 最新记录 RNN Bli bath size = 50  the accuracy is 0.989/ LSTM 在 bath size 50 之后的概率为 0.987

***1，2，3的优化方向***

更改特征处理代码

```python
vec = CountVectorizer()

X_train1 = vec.fit_transform(x_train)

X_test = vec.transform(x_valid)
```

我用的是这个，其实还可以自己手动处理数据。。

