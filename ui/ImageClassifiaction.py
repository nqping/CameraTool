#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/14 15:09
# @Author  : nqp
# @File    : ImageClassifiaction.py
# @Description : 图像检查，检查黑屏，椒盐噪声（雪花图），帧率
import sys

import cv2
import numpy as np
import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QApplication, QTextEdit, QMessageBox, QGroupBox, QTextBrowser, QLabel, QComboBox, QRadioButton

class ImageClassifiaction(QWidget):
    def __init__(self):
        super(ImageClassifiaction, self).__init__()
        self.resize(700, 500)
        self.setUpUI()

    def setUpUI(self):
        ############### 布局初始化 ##############################
        self.mainLayout = QVBoxLayout()  # 垂直布局
        self.Hlayout1 = QHBoxLayout()  # 水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        self.Hlayout5 = QHBoxLayout()
        self.Hlayout6 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        self.filePathInputEdit = QLineEdit()
        self.filePathInputEdit.setFixedHeight(32)
        self.filePathInputEdit.setPlaceholderText("图片路径")
        self.filePathInputEdit.setFont(font)

        self.inputDirBtn = QPushButton("选择目录")
        self.inputDirBtn.setObjectName("inputDirBtn")
        self.inputDirBtn.setFixedHeight(32)
        self.inputDirBtn.setFixedWidth(100)
        self.inputDirBtn.setFont(font)

        self.filePathOutEdit = QLineEdit()
        self.filePathOutEdit.setFixedHeight(32)
        self.filePathOutEdit.setPlaceholderText("输出目录,为空时自动创建")
        self.filePathOutEdit.setFont(font)

        self.outDirBtn = QPushButton("选择输出目录")
        self.outDirBtn.setObjectName("outDirBtn")
        self.outDirBtn.setFixedHeight(32)
        self.outDirBtn.setFixedWidth(100)
        self.outDirBtn.setFont(font)

        self.label_1 = QLabel("位置1 ")
        self.label_1.setFont(font)
        self.label_1.setFixedHeight(32)

        self.label_X0 = QLabel("X0：")
        self.label_X0.setFont(font)
        self.label_X0.setFixedHeight(32)

        self.label_X1 = QLabel("X1：")
        self.label_X1.setFont(font)
        self.label_X1.setFixedHeight(32)

        self.label_Y0 = QLabel("Y0：")
        self.label_Y0.setFont(font)
        self.label_Y0.setFixedHeight(32)

        self.label_Y1 = QLabel("Y1：")
        self.label_Y1.setFont(font)
        self.label_Y1.setFixedHeight(32)

        self.img_X0 = QLineEdit()
        self.img_X0.setFixedHeight(32)
        self.img_X0.setPlaceholderText("默认0")
        self.img_X0.setFont(font)

        self.img_X1 = QLineEdit()
        self.img_X1.setFixedHeight(32)
        self.img_X1.setPlaceholderText("默认0")
        self.img_X1.setFont(font)

        self.img_Y0 = QLineEdit()
        self.img_Y0.setFixedHeight(32)
        self.img_Y0.setPlaceholderText("默认0")
        self.img_Y0.setFont(font)

        self.img_Y1 = QLineEdit()
        self.img_Y1.setFixedHeight(32)
        self.img_Y1.setPlaceholderText("默认0")
        self.img_Y1.setFont(font)
#########################################################
        self.label_2 = QLabel("位置2 ")
        self.label_2.setFont(font)
        self.label_2.setFixedHeight(32)

        self.label_X0_2 = QLabel("X0：")
        self.label_X0_2.setFont(font)
        self.label_X0_2.setFixedHeight(32)

        self.label_X1_2 = QLabel("X1：")
        self.label_X1_2.setFont(font)
        self.label_X1_2.setFixedHeight(32)

        self.label_Y0_2 = QLabel("Y0：")
        self.label_Y0_2.setFont(font)
        self.label_Y0_2.setFixedHeight(32)

        self.label_Y1_2 = QLabel("Y1：")
        self.label_Y1_2.setFont(font)
        self.label_Y1_2.setFixedHeight(32)

        self.img_X0_2 = QLineEdit()
        self.img_X0_2.setFixedHeight(32)
        self.img_X0_2.setPlaceholderText("默认0")
        self.img_X0_2.setFont(font)

        self.img_X1_2 = QLineEdit()
        self.img_X1_2.setFixedHeight(32)
        self.img_X1_2.setPlaceholderText("默认0")
        self.img_X1_2.setFont(font)

        self.img_Y0_2 = QLineEdit()
        self.img_Y0_2.setFixedHeight(32)
        self.img_Y0_2.setPlaceholderText("默认0")
        self.img_Y0_2.setFont(font)

        self.img_Y1_2 = QLineEdit()
        self.img_Y1_2.setFixedHeight(32)
        self.img_Y1_2.setPlaceholderText("默认0")
        self.img_Y1_2.setFont(font)

        self.seachBtn = QPushButton("开始检索")
        self.seachBtn.setObjectName("seachBtn")
        self.seachBtn.setFixedHeight(32)
        self.seachBtn.setFont(font)

        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        self.logTextEdit = QTextBrowser()
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setPlaceholderText("Pring log ...")

        self.Hlayout1.addWidget(self.filePathInputEdit)
        self.Hlayout1.addWidget(self.inputDirBtn)
        self.Hlayout2.addWidget(self.filePathOutEdit)
        self.Hlayout2.addWidget(self.outDirBtn)

        self.Hlayout3.addWidget(self.label_1)
        self.Hlayout3.addWidget(self.label_X0)
        self.Hlayout3.addWidget(self.img_X0)
        self.Hlayout3.addWidget(self.label_Y0)
        self.Hlayout3.addWidget(self.img_Y0)
        self.Hlayout3.addWidget(self.label_X1)
        self.Hlayout3.addWidget(self.img_X1)
        self.Hlayout3.addWidget(self.label_Y1)
        self.Hlayout3.addWidget(self.img_Y1)

        self.Hlayout4.addWidget(self.label_2)
        self.Hlayout4.addWidget(self.label_X0_2)
        self.Hlayout4.addWidget(self.img_X0_2)
        self.Hlayout4.addWidget(self.label_Y0_2)
        self.Hlayout4.addWidget(self.img_Y0_2)
        self.Hlayout4.addWidget(self.label_X1_2)
        self.Hlayout4.addWidget(self.img_X1_2)
        self.Hlayout4.addWidget(self.label_Y1_2)
        self.Hlayout4.addWidget(self.img_Y1_2)

        self.Hlayout5.addWidget(self.seachBtn)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = ImageClassifiaction()
    rcp.show()
    sys.exit(app.exec_())