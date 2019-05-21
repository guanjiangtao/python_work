#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT
# file 模型文件

import paddle.fluid as fluid
import numpy as np 
import paddle as paddle
from PIL import Image
import os
import resnet as imageNetWork
import resnet_visit as visitNetWork

class MultiModel(object):
    def __init__(self):
        self.image = fluid.layers.data(name='image', shape=[3,88,88],dtype='float32')
        self.visit = fluid.layers.data(name='visit', shape=[7,26,24],dtype='float32')

        self.label = fluid.layers.data(name='label', shape=[1], dtype='int32')
        self.on_hot = fluid.layers.one_hot(input=self.label, depth=9)

        self.global_step = fluid.layers.create_parameter(name="global_step",shape=[1],dtype='float32')
        self.training = fluid.layers.data(dtype='bool',name='training',shape=[1])
        self.output_image = self.image_network(self.image)
        print(self.output_image)
        self.output_visit = self.visit_network(self.visit)
        print(self.output_visit)
        concat_list = [self.output_image,self.output_visit]
        self.output = fluid.layers.concat(input=concat_list,  axis=1)
        self.prediction = fluid.layers.fc(self.output,size=9)

        self.loss = self.get_loss(self.prediction, self.one_hot)  
        self.batch_size = 512
    
        self.correct_prediction = fluid.layers.equal('correct_prediction',fluid.layers.argmax(self.prediction, 1) == fluid.layers.argmax(self.one_hot, 1)) 
        self.accuracy = fluid.layers.reduce_mean('accuracy',fluid.layers.cast(correct_prediction, dtype="float32"))
          
        print(self.accuracy)

        self.optimizer = fluid.optimizer.AdamOptimizer(1e-3,1e-06,fluid.regularizer.L2DecayRegularizer,"optimizer",0.0004)
        # self.merged = tf.summary.merge_all()
        
        print("网络初始化成功")

    """
        图片网络
        @param image 图片
        @network Resnet-image
    """
    def image_network(self, image):
        return imageNetWork.ResNet().net(image)

    """
        访问数据网络
        @image image 图片
        @network Resnet-visit
    """
    def visit_network(self, image):
        return visitNetWork.ResNet().net(image)

    """
        获取损失值
    """
    def get_loss(self, output_concat, onhot):
        if self.stage == "loss":
            losses = fluid.layers.sigmoid_cross_entropy_with_logits(x=output_concat, label=onhot)
            loss = fluid.layers.reduce_mean(losses)
        return loss


if __name__ == "__main__":
    model = MultiModel()
    print(model)

    