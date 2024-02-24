#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 19:06
# @Author  : nqp
# @File    : cai2.py
# @Description :

import os
import cv2

##  img[y0:y1,x0:x1]  x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标

img = cv2.imread("5.png")
print("{},{}".format(img.shape[0],img.shape[1]))
# he = int(img.shape[0])  #0.085  纵向
# ve = 40 #int(img.shape[1] * 0.064)  # 0.064

#img = img[ve:] #裁上
#img = img[:-ve] #裁下
#img = img[ve:-ve] #裁上裁下
# img = img[:480, 40:] #裁左

# img = img[:480, 20:-20] #裁左右


# he = int(img.shape[0] * 0.1)
# ve = int(img.shape[1] * 0.1)
# print(he,ve)
img = img[:480, 40:] #裁左
# img = img[20:-20]

# he = int(img.shape[0] * 0.085)
# # ve = int(img.shape[1] * 0.1)
# img = img[he:-he]
cv2.imwrite("7.png",img)