#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 16:25
# @Author  : nqp
# @File    : ImageAlign.py
# @Description : 图像融合用来看对齐
"""
1.把16位的深度png图转换成8位的彩色可视化图像 (16位的是全黑图像）
2.转换后的深度png图与rgb图融合进行图像比对
"""
import os
import sys
import time
from pathlib import *

import cv2
import numpy as np
from PIL import Image
import qdarkstyle
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QApplication, QLineEdit, QPushButton, \
    QMessageBox, QFileDialog, QLabel, QComboBox,QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QMetaObject, pyqtSlot,QEvent

class ImageAlign(QWidget):

    def __init__(self,parent=None):
        super(ImageAlign,self).__init__(parent)
        self.resize(700, 500)
        self.setUpUI2()

    def setUpUI2(self):
        self.mainLayout = QVBoxLayout()  # 垂直布局
        self.Hlayout1 = QHBoxLayout()  # 水平布局
        self.Hlayout2 = QHBoxLayout()  # 水平布局
        self.Hlayout3 = QHBoxLayout()  # 水平布局
        self.Hlayout4 = QHBoxLayout()  # 水平布局
        self.Hlayout5 = QHBoxLayout()  # 水平布局
        self.Hlayout6 = QHBoxLayout()  # 水平布局

        font = QFont()
        font.setPixelSize(15)

        self.depth_path_edit = QLineEdit()
        self.depth_path_edit.setFixedHeight(32)
        self.depth_path_edit.setPlaceholderText("Depth路径，不支持中文路径")
        self.depth_path_edit.setFont(font)

        self.depth_path_Btn = QPushButton("Depth文件")
        self.depth_path_Btn.setObjectName("depth_path_Btn")
        self.depth_path_Btn.setFixedHeight(32)
        self.depth_path_Btn.setFixedWidth(100)
        self.depth_path_Btn.setFont(font)

        self.rgb_path_edit = QLineEdit()
        self.rgb_path_edit.setFixedHeight(32)
        self.rgb_path_edit.setPlaceholderText("RGB路径，不支持中文路径")
        self.rgb_path_edit.setFont(font)

        self.out_path_edit = QLineEdit()
        self.out_path_edit.setFixedHeight(32)
        self.out_path_edit.setPlaceholderText("输出路径")
        self.out_path_edit.setFont(font)

        self.out_path_Btn = QPushButton("输出目录")
        self.out_path_Btn.setObjectName("depth_path_Btn")
        self.out_path_Btn.setFixedHeight(32)
        self.out_path_Btn.setFixedWidth(100)
        self.out_path_Btn.setFont(font)


        self.img_size_label = QLabel("查看对齐效果请选择图片分辩率：")
        self.img_size_label.setFont(font)
        self.img_size_label.setFixedHeight(32)

        imgsize_data = ["640x480", "640x360","320x240","640x400"]
        self.imgSizeBox = QComboBox()
        self.imgSizeBox.addItems(imgsize_data)
        self.imgSizeBox.setCurrentIndex(0)
        self.imgSizeBox.setFixedHeight(32)
        self.imgSizeBox.setFont(font)

        self.rgb_path_Btn = QPushButton("RGB文件")
        self.rgb_path_Btn.setObjectName("rgb_path_Btn")
        self.rgb_path_Btn.setFixedHeight(32)
        self.rgb_path_Btn.setFixedWidth(100)
        self.rgb_path_Btn.setFont(font)

        self.convert_Btn = QPushButton("Depth转换灰色图")
        self.convert_Btn.setObjectName("convert_Btn")
        self.convert_Btn.setFixedHeight(32)
        self.convert_Btn.setFont(font)

        self.convert_Btn2 = QPushButton("Depth转彩色图")
        self.convert_Btn2.setObjectName("convert_Btn2")
        self.convert_Btn2.setFixedHeight(32)
        self.convert_Btn2.setFont(font)

        self.convert_Btn3 = QPushButton("Depth转点云")
        self.convert_Btn3.setObjectName("convert_Btn3")
        self.convert_Btn3.setFixedHeight(32)
        self.convert_Btn3.setFont(font)


        self.fusion_Btn = QPushButton("图片融合")
        self.fusion_Btn.setObjectName("fusion_Btn")
        self.fusion_Btn.setFixedHeight(32)
        self.fusion_Btn.setFont(font)

        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        self.groupBox0 = QGroupBox("单文件图像合并")
        self.groupBox0.setFlat(True)





        #打印日志
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setObjectName("logTextEdit")

        self.Hlayout1.addWidget(self.depth_path_edit)
        self.Hlayout1.addWidget(self.depth_path_Btn)

        self.Hlayout2.addWidget(self.rgb_path_edit)
        self.Hlayout2.addWidget(self.rgb_path_Btn)
        self.Hlayout3.addWidget(self.out_path_edit)
        self.Hlayout3.addWidget(self.out_path_Btn)

        self.Hlayout4.addWidget(self.img_size_label)
        self.Hlayout4.addWidget(self.imgSizeBox)
        self.Hlayout4.addWidget(self.fusion_Btn)


        self.Hlayout5.addWidget(self.convert_Btn)
        self.Hlayout5.addWidget(self.convert_Btn2)
        self.Hlayout5.addWidget(self.convert_Btn3)


        # self.Hlayout5.addWidget(self.fusion_Btn)
        self.Hlayout5.addWidget(self.clearBtn)
        self.Hlayout6.addWidget(self.logTextEdit)

        self.mainLayout.addLayout(self.Hlayout1)
        self.mainLayout.addLayout(self.Hlayout2)
        self.mainLayout.addLayout(self.Hlayout3)
        self.mainLayout.addLayout(self.Hlayout4)
        self.mainLayout.addLayout(self.Hlayout5)
        self.mainLayout.addLayout(self.Hlayout6)


        self.setLayout(self.mainLayout)

        QMetaObject.connectSlotsByName(self)

     ##########################按钮事件###################################

    @pyqtSlot()
    def on_clearBtn_clicked(self):
        self.logTextEdit.clear()


    @pyqtSlot()
    def on_depth_path_Btn_clicked(self):
        filePath= QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.depth_path_edit.setText(filePath)

    @pyqtSlot()
    def on_rgb_path_Btn_clicked(self):
        rgbPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.rgb_path_edit.setText(rgbPath)

    @pyqtSlot()
    def on_out_path_Btn_clicked(self):
        outPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.out_path_edit.setText(outPath)


    #图像对齐
    @pyqtSlot()
    def on_fusion_Btn_clicked(self):
        depth_path = self.depth_path_edit.text()
        rgb_path = self.rgb_path_edit.text()
        out_path = self.out_path_edit.text()
        img_size_data = self.imgSizeBox.currentText()
        img_size=img_size_data.split("x")#分隔出width和height

        if rgb_path == "" or depth_path == "":
            QMessageBox.warning(self, '警告', 'RGB 或 Depth 路径为空')
            return

        # 设置输出目录
        if out_path == "":
            out_path = PurePath(depth_path, "output")  # 拼接路径
            self.out_path_edit.setText(str(out_path))

        # 输出目录不存在则创建
        if not Path(out_path).exists():
            Path.mkdir(Path(out_path))

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.imgAlign,
                                       args=(depth_path, rgb_path,out_path,img_size[0],img_size[1]))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

    #Depth转换灰色图
    @pyqtSlot()
    def on_convert_Btn_clicked(self):
        input_path = self.depth_path_edit.text()
        out_path = self.out_path_edit.text()

        if input_path == "":
            QMessageBox.warning(self, '警告', 'Depth文件路径为空')
            return

        #设置输出目录
        if out_path =="":
            out_path = PurePath(input_path,"output")  #拼接路径
            self.out_path_edit.setText(str(out_path))

        # 输出目录不存在则创建
        if not Path(out_path).exists():
            Path.mkdir(Path(out_path))

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.converPngAll,
                                       args=(input_path, out_path))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

    ##Depth转换彩色图
    @pyqtSlot()
    def on_convert_Btn2_clicked(self):
        input_path = self.depth_path_edit.text()
        out_path = self.out_path_edit.text()

        if input_path == "":
            QMessageBox.warning(self, '警告', 'Depth文件路径为空')
            return

        # 设置输出目录
        if out_path == "":
            out_path = PurePath(input_path, "output")  # 拼接路径
            self.out_path_edit.setText(str(out_path))

        # 输出目录不存在则创建
        if not Path(out_path).exists():
            Path.mkdir(Path(out_path))

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.converPngForColored,
                                       args=(input_path, out_path))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

    ##Depth转点云
    @pyqtSlot()
    def on_convert_Btn3_clicked(self):
        input_path = self.depth_path_edit.text()
        out_path = self.out_path_edit.text()

        if input_path == "":
            QMessageBox.warning(self, '警告', 'Depth文件路径为空')
            return

        # 设置输出目录
        if out_path == "":
            out_path = PurePath(input_path, "output")  # 拼接路径
            self.out_path_edit.setText(str(out_path))

        # 输出目录不存在则创建
        if not Path(out_path).exists():
            Path.mkdir(Path(out_path))

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.depthToPointCloud,
                                       args=(input_path, out_path))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

    def enterEvent(self, event) -> None:
        pass

    def leaveEvent(self, event) -> None:
        pass

    ########################数据处理函数###################################
    def png2cloud(self, output, file, img):
        fx = 850 / 2
        fy = 850 / 2
        cx = 320
        cy = 200

        count = 0
        h, w = img.shape[:2]
        for y in range(h):
            for x in range(w):
                if img[y, x] > 0:
                    count += 1

        # save to cloud
        file_name = os.path.basename(file)
        file_name = file_name.split('.')[0]
        ply_path = os.path.join(output, '{}.ply'.format(file_name))
        ply = open(ply_path, 'w')
        print("ply", file=ply)
        print("format ascii 1.0", file=ply)
        print("comment VCGLIB generated", file=ply)
        print("element vertex {}".format(count), file=ply)
        print("property float x", file=ply)
        print("property float y", file=ply)
        print("property float z", file=ply)
        print("element face 0", file=ply)
        print("property list uchar int vertex_indices", file=ply)
        print("end_header", file=ply)
        for y in range(h):
            for x in range(w):
                value = img[y, x]
                if value > 0:
                    print('{:.3f} {:.3f} {:.3f}'.format(value * (1.00 * x - cx) / fx, value * (1.00 * y - cy) / fy,
                                                        value), file=ply)
        ply.close()

    def raw2cloud(self, output, file, img):
        fx = 850 / 2
        fy = 850 / 2
        cx = 320
        cy = 200

        w = 640
        h = 400
        count = 0
        for y in range(h):
            for x in range(w):
                if img[y * w + x] > 0:
                    count += 1

        # save to cloud
        file_name = os.path.basename(file)
        file_name = file_name.split('.')[0]
        ply_path = os.path.join(output, '{}.ply'.format(file_name))
        ply = open(ply_path, 'w')
        print("ply", file=ply)
        print("format ascii 1.0", file=ply)
        print("comment VCGLIB generated", file=ply)
        print("element vertex {}".format(count), file=ply)
        print("property float x", file=ply)
        print("property float y", file=ply)
        print("property float z", file=ply)
        print("element face 0", file=ply)
        print("property list uchar int vertex_indices", file=ply)
        print("end_header", file=ply)
        for y in range(h):
            for x in range(w):
                value = img[y * w + x]
                if value > 0:
                    print('{:.3f} {:.3f} {:.3f}'.format(value * (1.00 * x - cx) / fx, value * (1.00 * y - cy) / fy,
                                                        value), file=ply)
        ply.close()


    def depthToPointCloud(self, input_path, out_path):
        self.print_msg('Start convert depth to cloud: \n\n')

        files = os.listdir(input_path)
        for file in files:
            self.print_msg('Converting: {}.\n'.format(file))
            # Read depth png
            imgPath = os.path.join(input_path, file)
            try:
                if file.endswith(".png"):
                    img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
                    self.png2cloud(out_path, file, img)
                elif file.endswith(".raw"):
                    img = np.fromfile(imgPath, dtype=np.uint16)
                    self.raw2cloud(out_path, file, img)
                else:
                    continue
            except:
                self.print_msg('Converting: {} failed.\n'.format(file))
                continue

        self.print_msg('\nEnd convert depth to cloud!')
        pass


    def converPngAll(self,input_path,out_path):
        try:
            for files in Path(input_path).glob(f"*"):  #不读取子文件夹
                if files.is_file():
                    #读取png文件
                    depth = cv2.imdecode(np.fromfile(files, dtype=np.uint8), -1)  #支持中文路径
                    xmin = 0
                    xmax = np.max(depth)

                    np.seterr(divide='ignore', invalid='ignore')  # 忽略0除以0的的警告
                    depth_image = np.array((depth - xmin) / (xmax - xmin) * 255).astype(np.uint8)
                    im = Image.fromarray(depth_image)
                    im.save(Path(out_path,files.name))
                    self.print_msg('Converting: {}.\n'.format(files.name))
            self.print_msg('\nEnd convert depth to png!')
        except Exception as e:
            self.print_msg('\nError:{} '.format(e))

    #将深度图转换成彩色图
    def converPngForColored(self,input_path,out_path):
        try:
            # files = os.listdir(input_path)
            # for file in files:
            #
            #     #读取深度图文件
            #     depth_image = cv2.imread(os.path.join(input_path,file),cv2.IMREAD_GRAYSCALE)
            #     # 将深度为0的像素置为NaN
            #     depth_image = depth_image.astype(float)
            #     depth_image[depth_image == 0] = np.nan
            #     # 将深度图像转换为伪彩色图像
            #     colored_depth = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=255/np.nanmax(depth_image)), cv2.COLORMAP_JET)
            #     # 将深度为0的像素显示为黑色
            #     colored_depth[np.isnan(depth_image)] = (0, 0, 0)
            #     cv2.imwrite(os.path.join(out_path,file), colored_depth)
            #     # self.print_msg('Converting: {}.\n'.format(files.name))
            # self.print_msg('\nEnd ............!')

            for files in Path(input_path).glob(f"*"):  #不读取子文件夹
                if files.is_file():
                    #读取深度图文件
                    depth_image = cv2.imread(str(files),cv2.IMREAD_GRAYSCALE)
                    # 将深度为0的像素置为NaN
                    depth_image = depth_image.astype(float)
                    depth_image[depth_image == 0] = np.nan
                    # 将深度图像转换为伪彩色图像
                    colored_depth = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=255/np.nanmax(depth_image)), cv2.COLORMAP_JET)
                    # 将深度为0的像素显示为黑色
                    colored_depth[np.isnan(depth_image)] = (0, 0, 0)
                    cv2.imwrite(os.path.join(out_path,files.name),colored_depth)
                    self.print_msg('Converting: {}.\n'.format(files.name))
            self.print_msg('\nEnd ............!')

        except Exception as e:
            self.print_msg('\nError:{} '.format(e))


    def imgAlign(self,depth_path,rgb_path,out_path,width,height):
        depth_list=[]
        rgb_list=[]

        [depth_list.append(str(f)) for f in Path(depth_path).glob(f"*") if Path(f).is_file()]
        [rgb_list.append(str(f)) for f in Path(rgb_path).glob(f"*") if Path(f).is_file()]

        #
        for i in range(len(depth_list)):
            # print(depth_list[i])
            depth_img = cv2.imread(depth_list[i])
            rgb_img = cv2.imread(rgb_list[i])
            # depth_img = cv2.imdecode(np.fromfile(depth_list[i],dtype=np.uint16),-1)
            # rgb_img = cv2.imdecode(np.fromfile(rgb_list[i],dtype=np.uint16),-1)

            # 图像融合
            combine = cv2.addWeighted(cv2.resize(depth_img, (int(width), int(height))), 0.5, cv2.resize(rgb_img, (int(width), int(height))),
                                      0.5, 0)
            out_img_name = PurePath(out_path, depth_list[i].split("\\")[-1])
            cv2.imwrite(str(out_img_name),combine)
            self.print_msg("{}与{}".format(depth_list[i],rgb_list[i]))
        self.print_msg('\nEnd ............!')

    def print_msg(self, msg):
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = ImageAlign()
    rcp.setWindowTitle("图像对齐")
    rcp.show()
    sys.exit(app.exec_())

