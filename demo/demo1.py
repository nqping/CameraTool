#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 14:53
# @Author  : nqp
# @File    : demo1.py
# @Description : 
import os,cv2
import re,shutil

path = r"E:\temp\Nuwa-HP60C\songyang\20230315-2\ASC60CC48000021\depth"
targetDir = r'E:\temp\result\out'


def getfilelist(strn):
    names = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            #             image_name=os.path.join(dirpath, filepath)#获取文件的全路径
            image_name = filepath
            str1 = re.compile(strn + '''(.*?).png''')
            match_obj = re.findall(str1, image_name)
            if match_obj:
                print(image_name)
                names.append(image_name)
                shutil.copy(image_name,  targetDir) #复制到另一个路径
    return names

def getImgType():
    path=r"0.raw"
    img = cv2.imread(path)
    size = img.shape
    print(size)
    print("高：%s"%size[0])
    print("宽：%s"%size[1])


if __name__=="__main__":
    # getfilelist('depth')
    getImgType()