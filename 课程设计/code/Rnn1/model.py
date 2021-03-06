#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT

import paddle.fluid as fluid

"""
    max acc 0.653

"""
def cnn_net(data,
            label,
            dict_dim,
            class_dim,
            emb_dim=128,
            hid_dim=128,
            hid_dim2=96,
            win_size=3,
            is_infer=False):
    # embedding layer
    emb = fluid.layers.embedding(input=data, size=[dict_dim, emb_dim])
    # convolution layer
    conv_3 = fluid.nets.sequence_conv_pool(
        input=emb,
        num_filters=hid_dim,
        filter_size=win_size,
        act="tanh",
        pool_type="max")
    # full connect layer
    fc_1 = fluid.layers.fc(input=[conv_3], size=hid_dim2)

    batch_normal = fluid.layers.batch_norm(input=fc_1,act="tanh")

    # softmax layer
    prediction = fluid.layers.fc(input=[batch_normal], size=class_dim, act="softmax")

    return prediction