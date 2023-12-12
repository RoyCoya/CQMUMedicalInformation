# 判断一张手骨图是不是“过暗”
# 注：暂时用不着了，现在用dicom自带的窗宽窗位tag进行压缩

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def create_hist(img, index):
    # 初始化一个字典来放数据,每个 key 的初始值都是 0，后面将这个图进行统计
    light_pixels = 0
    for i in range(0,len(img),2):
        for j in range(0,len(img[1]),2):
            if img[i][j] >= 70:
                light_pixels += 1
    x_len = int((len(img[0]) - 0)/2) + 1
    y_len = int((len(img) - 0)/2) + 1
    light_ratio = light_pixels/(x_len * y_len)
    is_dark = False
    if light_ratio < 0.02:
        is_dark = True
    print(index, is_dark)

# 图片读取
for i in range(1,148):
    url = os.getcwd()+'/' + str(i) + '.png'
    img = cv2.imread(url, 0)  # 后面模式为 0 可以直接读成灰度图
    create_hist(img, i)