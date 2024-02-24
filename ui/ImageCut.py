#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 17:53
# @Author  : nqp
# @File    : ImageCut.py
# @Description : 图片裁切
##裁剪坐标为img[y0:y1, x0:x1]
import sys
import threading
import time
from pathlib import Path, PurePath

import cv2
import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextBrowser, QApplication, \
    QComboBox, QLabel, QFileDialog, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QFont

class ImageCut(QWidget):
    def __init__(self):
        super(ImageCut, self).__init__()
        self.resize(700, 500)
        self.setUpUI()

    def setUpUI(self):
        self.mainLayout = QVBoxLayout()  # 垂直布局
        self.Hlayout1 = QHBoxLayout()  # 水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        self.Hlayout5 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        self.input_dir_edit = QLineEdit()
        self.input_dir_edit.setFixedHeight(32)
        self.input_dir_edit.setPlaceholderText("输入图片目录")
        self.input_dir_edit.setFont(font)

        self.inputDirBtn = QPushButton("选择输入目录")
        self.inputDirBtn.setObjectName("inputDirBtn")
        self.inputDirBtn.setFixedHeight(32)
        self.inputDirBtn.setFixedWidth(100)
        self.inputDirBtn.setFont(font)

        self.out_dir_edit = QLineEdit()
        self.out_dir_edit.setFixedHeight(32)
        self.out_dir_edit.setPlaceholderText("输出目录,为空时自动创建")
        self.out_dir_edit.setFont(font)

        self.outDirBtn = QPushButton("输出目录")
        self.outDirBtn.setObjectName("outDirBtn")
        self.outDirBtn.setFixedHeight(32)
        self.outDirBtn.setFixedWidth(100)
        self.outDirBtn.setFont(font)

        self.label_up = QLabel("上：")
        self.label_up.setFont(font)
        self.label_up.setFixedHeight(32)

        self.label_down = QLabel("下：")
        self.label_down.setFont(font)
        self.label_down.setFixedHeight(32)

        self.label_left = QLabel("左：")
        self.label_left.setFont(font)
        self.label_left.setFixedHeight(32)

        self.label_right = QLabel("右：")
        self.label_right.setFont(font)
        self.label_right.setFixedHeight(32)

        self.img_cut_up = QLineEdit()
        self.img_cut_up.setFixedHeight(32)
        self.img_cut_up.setPlaceholderText("默认0")
        self.img_cut_up.setFont(font)

        self.img_cut_down = QLineEdit()
        self.img_cut_down.setFixedHeight(32)
        self.img_cut_down.setPlaceholderText("默认0")
        self.img_cut_down.setFont(font)

        self.img_cut_left = QLineEdit()
        self.img_cut_left.setFixedHeight(32)
        self.img_cut_left.setPlaceholderText("默认0")
        self.img_cut_left.setFont(font)

        self.img_cut_right = QLineEdit()
        self.img_cut_right.setFixedHeight(32)
        self.img_cut_right.setPlaceholderText("默认0")
        self.img_cut_right.setFont(font)

        self.img_rgb = QRadioButton("RGB",self)
        self.img_depth = QRadioButton("Depth",self)
        self.img_rgb.setChecked(True)

        self.gbBtn = QButtonGroup(self)
        self.gbBtn.setObjectName("gbBtn")
        self.gbBtn.addButton(self.img_rgb,1)
        self.gbBtn.addButton(self.img_depth,2)


        self.cutBtn = QPushButton("裁切")
        self.cutBtn.setObjectName("cutBtn")
        self.cutBtn.setFixedHeight(32)
        self.cutBtn.setFont(font)

        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        self.logTextEdit = QTextBrowser()
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setPlaceholderText("Pring log ...")

        self.Hlayout1.addWidget(self.input_dir_edit)
        self.Hlayout1.addWidget(self.inputDirBtn)
        self.Hlayout2.addWidget(self.out_dir_edit)
        self.Hlayout2.addWidget(self.outDirBtn)
        self.Hlayout3.addWidget(self.label_up)
        self.Hlayout3.addWidget(self.img_cut_up)
        self.Hlayout3.addWidget(self.label_down)
        self.Hlayout3.addWidget(self.img_cut_down)
        self.Hlayout3.addWidget(self.label_left)
        self.Hlayout3.addWidget(self.img_cut_left)
        self.Hlayout3.addWidget(self.label_right)
        self.Hlayout3.addWidget(self.img_cut_right)
        self.Hlayout3.addWidget(self.img_depth)
        self.Hlayout3.addWidget(self.img_rgb)
        self.Hlayout4.addWidget(self.cutBtn)
        self.Hlayout4.addWidget(self.clearBtn)
        self.Hlayout5.addWidget(self.logTextEdit)

        self.mainLayout.addLayout(self.Hlayout1)
        self.mainLayout.addLayout(self.Hlayout2)
        self.mainLayout.addLayout(self.Hlayout3)
        self.mainLayout.addLayout(self.Hlayout4)
        self.mainLayout.addLayout(self.Hlayout5)

        self.setLayout(self.mainLayout)
        QMetaObject.connectSlotsByName(self)

#########################Btn按钮事件##################################
    @pyqtSlot()
    def on_inputDirBtn_clicked(self):
        inputDir = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.input_dir_edit.setText(inputDir)

    @pyqtSlot()
    def on_outDirBtn_clicked(self):
        outDir = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.out_dir_edit.setText(outDir)

    @pyqtSlot()
    def on_clearBtn_clicked(self):
        self.logTextEdit.clear()


    @pyqtSlot()
    def on_cutBtn_clicked(self):
        inputPath = self.input_dir_edit.text().strip()
        outPath = self.out_dir_edit.text().strip()

        up = self.img_cut_up.text().strip()
        down = self.img_cut_down.text().strip()
        left = self.img_cut_left.text().strip()
        right = self.img_cut_right.text().strip()
        imgType  = self.gbBtn.checkedId()  #1:RGB 2:Depth

        if inputPath == "":
            QMessageBox.warning(self, '警告', '输入路径为空')
            return
        elif not Path(inputPath).exists():
            QMessageBox.warning(self, '警告', '路径不存在')
            return

        if outPath == "":
            outPath = PurePath(inputPath, "output")  # 拼接路径
        self.out_dir_edit.setText(str(outPath))

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.cutImages,args=(inputPath, outPath, up, down, left, right,imgType))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

########################数据处理函数###################################
    def cutImages(self,inputDir,outDir,up,down,left,right,imgType):
        if not Path(outDir).exists():
            Path.mkdir(Path(outDir))

        if imgType == 1:
            for file in Path(inputDir).glob(f"*"):  #不取子目录
                if file.is_file():
                    img = cv2.imread(str(file),cv2.IMREAD_ANYCOLOR)
                    size = img.shape
                    outImg = self.handleImg(img,size[1],size[0],up,down,left,right)
                    outDir = PurePath(outDir,file.name)
                    cv2.imwrite(str(outDir), outImg)
                    self.print_msg('{}->{}x{} '.format(file,size[1], size[0]))

        else:
            for file in Path(inputDir).glob(f"*"):  # 不取子目录
                if file.is_file():
                    img = cv2.imread(str(file), cv2.IMREAD_ANYDEPTH)
                    size = img.shape
                    outImg = self.handleImg(img, size[1], size[0], up, down, left, right)
                    outDir = PurePath(outDir, file.name)
                    cv2.imwrite(str(outDir), outImg)
                    self.print_msg('{}->{}x{} '.format(file, size[1], size[0]))


    def handleImg(self,img,width,height,up,down,left,right):
        #裁剪坐标为img[y0:y1, x0:x1]
        if up !="" and down =="" and left=="" and right=="": #裁上
            img = img[int(up):]

        elif down !="" and up =="" and left=="" and right=="": #裁下
            img = img[:-int(down)]

        elif up!="" and down !="" and left=="" and right=="":#裁上下
            img = img[int(up):-int(down)]

        elif up =="" and down =="" and left!="" and right=="": #裁左
            img = img[:int(height),int(left):]

        elif up =="" and down =="" and left=="" and right !="":#裁右
            img = img[:int(height), :-int(right)]

        elif up =="" and down =="" and left !="" and right !="":#裁左右
            img = img[:int(height), int(left):-int(right)]

        elif up !="" and down !="" and left !="" and right !="":#裁上下左右
            img = img[int(up):-int(down), int(left):-int(right)]

        return img

    def print_msg(self, msg):
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = ImageCut()
    rcp.show()
    sys.exit(app.exec_())