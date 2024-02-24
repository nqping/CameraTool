#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 17:48
# @Author  : nqp
# @File    : FileConversion.py
# @Description : （bin、yuv、raw）转换成png
import os
import re
import shutil
import sys
import threading
import time
from pathlib import Path, PurePath


import cv2
import numpy as np
import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QApplication, QTextEdit, QMessageBox, QGroupBox, QTextBrowser, QLabel, QComboBox, QRadioButton


class ChangeFile(QWidget):

    def __init__(self):
        super(ChangeFile, self).__init__()
        self.resize(700, 500)
        self.setUpUI()

    def setUpUI(self):
        ############### 布局初始化 ##############################
        self.layout = QVBoxLayout()  # 垂直布局
        self.Hlayout1 = QHBoxLayout()  # 水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        self.Hlayout5 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        self.filePathInputEdit = QLineEdit()
        self.filePathInputEdit.setFixedHeight(32)
        self.filePathInputEdit.setPlaceholderText("输入目录,不支持中文路径")
        self.filePathInputEdit.setFont(font)

        self.filePathOutEdit = QLineEdit()
        self.filePathOutEdit.setFixedHeight(32)
        self.filePathOutEdit.setPlaceholderText("输出目录,为空时自动创建")
        self.filePathOutEdit.setFont(font)

        self.inputDirBtn = QPushButton("选择输入目录")
        self.inputDirBtn.setObjectName("inputDirBtn")
        self.inputDirBtn.setFixedHeight(32)
        self.inputDirBtn.setFont(font)

        self.outDirBtn = QPushButton("选择输出目录")
        self.outDirBtn.setObjectName("outDirBtn")
        self.outDirBtn.setFixedHeight(32)
        self.outDirBtn.setFont(font)

        self.RGB_radio = QRadioButton("RGB")
        self.RGB_radio.setObjectName("RGB_radio")

        self.Depth_radio = QRadioButton("Depth")
        self.Depth_radio.setObjectName("Depth_radio")
        self.Depth_radio.setChecked(True)


        suffiex_data = [".raw", ".bin", ".yuv"]
        self.suffixBox = QComboBox()
        self.suffixBox.addItems(suffiex_data)
        self.suffixBox.setCurrentIndex(0)
        self.suffixBox.setFixedHeight(32)
        self.suffixBox.setFixedWidth(100)
        self.suffixBox.setFont(font)

        self.label1 = QLabel("转 png")
        self.label1.setFont(font)
        self.label1.setFixedHeight(32)

        self.label_w = QLabel("width：")
        self.label_w.setFont(font)
        self.label_w.setFixedHeight(32)

        self.width_edit = QLineEdit()
        self.width_edit.setObjectName("width_edit")
        self.width_edit.setPlaceholderText("图像宽或行数")
        self.width_edit.setFont(font)
        self.width_edit.setFixedHeight(32)

        self.label_h = QLabel("height：")
        self.label_h.setFont(font)
        self.label_h.setFixedHeight(32)

        self.height_edit = QLineEdit()
        self.height_edit.setObjectName("height_edit")
        self.height_edit.setPlaceholderText("图像高或列数")
        self.height_edit.setFont(font)
        self.height_edit.setFixedHeight(32)

        self.start_btn = QPushButton("开始转换")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setFixedHeight(32)
        self.start_btn.setFont(font)

        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        self.logTextEdit = QTextBrowser()
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setPlaceholderText("Pring log ...")

        # self.RGB_radio.toggled.connect(self.buttonState)
        # self.Depth_radio.toggled.connect(self.buttonState)

        ################# 将控制加入到子布局中 #############################
        self.Hlayout1.addWidget(self.filePathInputEdit)
        self.Hlayout1.addWidget(self.inputDirBtn)
        self.Hlayout2.addWidget(self.filePathOutEdit)
        self.Hlayout2.addWidget(self.outDirBtn)

        self.Hlayout3.addWidget(self.RGB_radio)
        self.Hlayout3.addWidget(self.Depth_radio)
        self.Hlayout3.addWidget(self.suffixBox)
        self.Hlayout3.addWidget(self.label1)


        self.Hlayout3.addWidget(self.label_w)
        self.Hlayout3.addWidget(self.width_edit)
        self.Hlayout3.addWidget(self.label_h)
        self.Hlayout3.addWidget(self.height_edit)

        self.Hlayout4.addWidget(self.start_btn)
        self.Hlayout4.addWidget(self.clearBtn)

        self.Hlayout5.addWidget(self.logTextEdit)

        ################### 将子布局加入主布局内 ###########################
        self.layout.addLayout(self.Hlayout1)
        self.layout.addLayout(self.Hlayout2)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout4)
        self.layout.addLayout(self.Hlayout5)

        self.setLayout(self.layout)

        QMetaObject.connectSlotsByName(self)



#######################按钮事件#############################################


    @pyqtSlot()
    def on_outDirBtn_clicked(self):
        out_path = QFileDialog.getExistingDirectory(self, "选择文件夹")


        self.filePathOutEdit.setText(out_path)

    @pyqtSlot()
    def on_inputDirBtn_clicked(self):
        input_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.filePathInputEdit.setText(input_path)

    @pyqtSlot()
    def on_clearBtn_clicked(self):
        self.logTextEdit.clear()

    @pyqtSlot()
    def on_start_btn_clicked(self):
        input_path = self.filePathInputEdit.text().strip()
        out_path = self.filePathOutEdit.text().strip()
        scr_suffix = self.suffixBox.currentText()
        img_type = 2  #1:RGB ,2：Depth
        if self.Depth_radio.isChecked():
            img_type=2

        if self.RGB_radio.isChecked():
            img_type = 1

        str_w = self.width_edit.text().strip()
        str_h = self.height_edit.text().strip()

        if input_path=="":
            QMessageBox.warning(self, '警告', '输入路径为空')
            return
        elif not Path(input_path).exists():
            QMessageBox.warning(self, '警告', '路径不存在')
            return

        if Path(out_path).exists():
            out_path = PurePath(input_path, "output")  # 拼接路径
        self.filePathOutEdit.setText(str(out_path))

        #宽和高输入验证
        if str_w!="" or str_h !="":
            match_obj_w = re.findall("^\d+$", str_w)
            match_obj_h = re.findall("^\d+$", str_h)
            if not match_obj_w or not match_obj_h:
                QMessageBox.warning(self, '警告', '高或宽必须是有效数字！')
                return
        else:
            QMessageBox.warning(self, '警告', '请输入高或宽！')
            return

        # 清空日志
        self.logTextEdit.clear()

        self.thread = threading.Thread(target=self.changFile,args=(input_path,out_path,scr_suffix,int(str_w),int(str_h),img_type))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()


########################事件函数############################################
    def changFile(self,input_path,out_path,scr_suffix,w,h,img_type):
        self.print_msg('Start convert depth to png: \n\n')
        if not Path(out_path).exists():
            Path.mkdir(Path(out_path))

        #RGB类型的yuv转png
        if img_type == 1:
            for file in Path(input_path).glob(f"*"):
                if file.is_file():
                    if file.suffix == scr_suffix:
                        img = np.fromfile(str(file), dtype='uint8')
                        img = img.reshape(h, w, 3) #高、宽、通道数
                        file_name = file.name.replace(scr_suffix, ".png")
                        out_img_path = PurePath(out_path, file_name)
                        cv2.imwrite(str(out_img_path), img)
                        self.print_msg('Converting: {}.\n'.format(file.name))

        else:
            #Depth类型yuv转png
            for file in Path(input_path).glob(f"*"):
                if file.is_file():
                    if file.suffix == scr_suffix:
                        img = np.fromfile(str(file), dtype=np.uint16)
                        img = img.reshape(h, w, 1)
                        file_name = file.name.replace(scr_suffix, ".png")
                        out_img_path = PurePath(out_path, file_name)
                        print(str(out_img_path))
                        cv2.imwrite(str(out_img_path), img)
                        self.print_msg('Converting: {}.\n'.format(file.name))

        self.print_msg('\nEnd convert depth to png!')


    def print_msg(self, msg):
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = ChangeFile()
    rcp.setWindowTitle("转换png")
    rcp.show()
    sys.exit(app.exec_())