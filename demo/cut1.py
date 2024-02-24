#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 18:20
# @Author  : nqp
# @File    : cut1.py
# @Description : 

import cv2

img = cv2.imread("6.png")


cv2.imshow("Original Image", img)

height, width = img.shape[:2]    #img.shape ：高、宽、通道
print(img.shape)
print(height, width)


start_row, start_col = int(width * 0.1), int(height * 0.1)
end_row, end_col = int(width * 0.1), int(height * 0.1)

##  img[y0:y1,x0:x1]  x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标

# cropped = img[start_row:end_row,start_col:end_col]
# # cropped=img[start_row:end_row,start_col:end_col]
# cropped = img[start_row:-start_row, start_col:-start_col] # 裁剪坐标为[y0:y1, x0:x1]
cropped = img[start_row:-start_row]

cv2.imwrite("7.png",cropped)
#
cv2.imshow("Cropped_Image", cropped)
#
cv2.waitKey(0)
cv2.destroyAllWindows()





# import cv2
#
# img = cv2.imread("./cut/1.jpg")
# print(img.shape)
# cropped = img[0:800, 88:712]  # 裁剪坐标为[y0:y1, x0:x1]
# cv2.imwrite("./out/1_o.jpg", cropped)
#
