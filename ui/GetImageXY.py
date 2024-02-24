#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 14:10
# @Author  : nqp
# @File    : GetImageXY.py
# @Description : 指定位置获取截图坐标

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

class GetImageXY(QWidget):
    def __init__(self):
        super(GetImageXY, self).__init__()
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

        self.inFileEdit = QLineEdit()
        self.inFileEdit.setFixedHeight(32)
        self.inFileEdit.setPlaceholderText("图片路径")
        self.inFileEdit.setFont(font)

        self.inputFileBtn = QPushButton("选择文件")
        self.inputFileBtn.setObjectName("inputFileBtn")
        self.inputFileBtn.setFixedWidth(100)
        self.inputFileBtn.setFixedHeight(32)
        self.inputFileBtn.setFont(font)

        # self.outFileEdit = QLineEdit()
        # self.outFileEdit.setFixedHeight(32)
        # self.outFileEdit.setPlaceholderText("输出目录")
        # self.outFileEdit.setFont(font)
        #
        # self.outFileBtn = QPushButton("选择输入目录")
        # self.outFileBtn.setObjectName("outFileBtn")
        # self.outFileBtn.setFixedWidth(100)
        # self.outFileBtn.setFixedHeight(32)
        # self.outFileBtn.setFont(font)

        self.start_btn = QPushButton("开始")
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

        self.Hlayout1.addWidget(self.inFileEdit)
        self.Hlayout1.addWidget(self.inputFileBtn)
        # self.Hlayout2.addWidget(self.outFileEdit)
        # self.Hlayout2.addWidget(self.outFileBtn)

        self.Hlayout3.addWidget(self.start_btn)
        self.Hlayout3.addWidget(self.clearBtn)

        self.Hlayout4.addWidget(self.logTextEdit)

        self.layout.addLayout(self.Hlayout1)
        # self.layout.addLayout(self.Hlayout2)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout4)

        self.setLayout(self.layout)

        QMetaObject.connectSlotsByName(self)

##########################按钮事件###################################
    @pyqtSlot()
    def on_clearBtn_clicked(self):
        self.logTextEdit.clear()

    @pyqtSlot()
    def on_inputFileBtn_clicked(self):
        inFilePath,filetype = QFileDialog.getOpenFileName(self,"选择一张图片","","Imge files(*.jpg *.png *.gif)")
        self.inFileEdit.setText(inFilePath)

    @pyqtSlot()
    def on_start_btn_clicked(self):
        filePath = self.inFileEdit.text()

        if filePath == "":
            QMessageBox.warning(self, '警告', '图片路径为空！')
            return

        img = cv2.imread(filePath)
        cv2.imshow('original', img)
        # cv2.waitKey()

        # 选择ROI
        roi = cv2.selectROI(windowName="original", img=img, showCrosshair=True, fromCenter=False)
        x, y, w, h = roi
        self.print_msg("截图坐标：X0={},Y0={}, X1={},Y1={}".format(x, y, x + w, y + h))

##########################函数处理###################################

    def print_msg(self,msg):
        time.sleep(0.02)
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = GetImageXY()
    rcp.setWindowTitle("截图坐标")
    rcp.show()
    sys.exit(app.exec_())



