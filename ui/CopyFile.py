#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 10:33
# @Author  : nqp
# @File    : RenameFile.py
# @Description : 从原始路径复制文件到目标路径
import re
import shutil
import sys,os
import threading
import time
from pathlib import Path, PurePath

import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QApplication,QTextEdit,QMessageBox,QGroupBox,QComboBox,QTextBrowser


class CopyFile(QWidget):

    def __init__(self):
        super(CopyFile,self).__init__()
        self.resize(700, 500)
        self.setUpUI()


    def setUpUI(self):
        self.layout = QVBoxLayout()  #垂直布局
        self.Hlayout1 = QHBoxLayout()  #水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        self.Hlayout5 = QHBoxLayout()
        # self.groupbox1 = QGroupBox("路径最后-级文件夹名重命名单个文件",self)

        font = QFont()
        font.setPixelSize(15)

        # Hlayout1控件的初始化
        self.filePathInputEdit = QLineEdit()
        self.filePathInputEdit.setFixedHeight(32)
        self.filePathInputEdit.setPlaceholderText("输入目录")
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

        self.regexEdit = QLineEdit()
        self.regexEdit.setObjectName("regexEdit")
        self.regexEdit.setPlaceholderText("非必填项,正则表达式如depth(.*?).png 复制包含depth的png格式文件，默认为空")
        self.regexEdit.setFixedHeight(32)
        self.regexEdit.setFont(font)

        suffiex_data=[".png",".raw",".bin",".jpg",".yuv"]
        self.suffixBox = QComboBox()
        self.suffixBox.addItems(suffiex_data)
        self.suffixBox.setCurrentIndex(0)
        self.suffixBox.setFixedHeight(32)
        self.suffixBox.setFont(font)

        self.startBtn = QPushButton("复制文件")
        self.startBtn.setObjectName("startBtn")
        self.startBtn.setFixedHeight(32)
        self.startBtn.setFont(font)

        self.moveBtn = QPushButton("移动文件")
        self.moveBtn.setObjectName("moveBtn")
        self.moveBtn.setFixedHeight(32)
        self.moveBtn.setFont(font)

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

        self.Hlayout3.addWidget(self.regexEdit)
        self.Hlayout4.addWidget(self.suffixBox)
        self.Hlayout4.addWidget(self.startBtn)
        self.Hlayout4.addWidget(self.moveBtn)
        self.Hlayout4.addWidget(self.clearBtn)

        self.Hlayout5.addWidget(self.logTextEdit)

        # Hlayout2初始化
        self.layout.addLayout(self.Hlayout1)
        self.layout.addLayout(self.Hlayout2)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout4)
        self.layout.addLayout(self.Hlayout5)

        self.setLayout(self.layout)

        QMetaObject.connectSlotsByName(self)

    #############Btn按钮事件#####################################
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
    def on_startBtn_clicked(self):

        input_path = self.filePathInputEdit.text()
        out_path = self.filePathOutEdit.text()
        suffix = self.suffixBox.currentText()
        regex_str = self.regexEdit.text()  #正则表达式

        if input_path=="":
            QMessageBox.warning(self, '警告', '输入路径为空')
            return
        elif not Path(input_path).exists():
            QMessageBox.warning(self, '警告', '路径不存在')
            return

        if out_path =="":
            out_path = PurePath(input_path,"output")  #拼接路径
            self.filePathOutEdit.setText(str(out_path))

        #清空日志
        self.logTextEdit.clear()

        self.thread = threading.Thread(target=self.copyFile, args=(input_path, out_path, suffix,regex_str))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

        # self.copyFile(input_path,out_path,suffix)

    @pyqtSlot()
    def on_moveBtn_clicked(self):

        input_path = self.filePathInputEdit.text()
        out_path = self.filePathOutEdit.text()
        suffix = self.suffixBox.currentText()
        regex_str = self.regexEdit.text()  # 正则表达式

        if input_path=="":
            QMessageBox.warning(self, '警告', '输入路径为空')
            return

        if out_path =="":
            QMessageBox.warning(self, '警告', '输出路径不存在')
            return

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.moveFiles, args=(input_path, out_path, suffix, regex_str))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()



###############################函数集###########################################################

    def print_msg(self,msg):
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部

    #复制文件
    def copyFile(self,src_dir,out_dir,suffix_cb,regex_str):
        if not Path(out_dir).exists():
            Path.mkdir(Path(out_dir))
        #正则表达式过虑复制
        if regex_str !="":
            str1 = re.compile(regex_str)
            for file in Path(src_dir).glob(f"*"):  #不读取子文件夹
                if file.is_file():
                    match_obj = re.findall(str1, file.name)
                    if match_obj:
                        try:
                            shutil.copy(file, Path(out_dir, file.name))
                            self.print_msg("{} 处理完成".format(file))
                        except shutil.SameFileError as sfe:
                            pass

        else:
            for file in Path(src_dir).glob(f"*"): #不读取子文件夹
                if file.is_file():
                    if file.suffix ==suffix_cb:  #取文件后缀名对比
                        try:
                            shutil.copy(file, Path(out_dir, file.name))
                            # print("{} 处理完成".format(file))
                            self.print_msg("{} 处理完成".format(file))
                        except shutil.SameFileError as sfe:
                            pass
        self.print_msg('\nEnd！')

    #移动文件
    def moveFiles(self,src_dir,out_dir,suffix_cb,regex_str):
        #输出路径没有则创建
        if not Path(out_dir).exists():
            Path.mkdir(Path(out_dir))

        if regex_str !="":
            str1 = re.compile(regex_str)
            for file in Path(src_dir).glob(f"*"):  #不读取子文件夹
                if file.is_file():
                    match_obj = re.findall(str1, file.name)
                    if match_obj:
                        try:
                            shutil.move(file,Path(out_dir,file.name))
                            self.print_msg("{} 处理完成".format(file))
                        except shutil.SameFileError as sfe:
                            self.print_msg(sfe)

        else:
            for file in Path(src_dir).glob(f"*"):  #不读取子文件夹
                if file.is_file():
                    if file.suffix == suffix_cb:  # 取文件后缀名对比
                        try:
                            shutil.move(file, Path(out_dir, file.name))
                            # print("{} 处理完成".format(file))
                            self.print_msg("{} 处理完成".format(file))
                        except shutil.SameFileError as sfe:
                            self.print_msg(sfe)

        self.print_msg('\nEnd！')




    # @pyqtSlot()
    # def on_renameBtn_clicked(self):
    #     input_path = self.filePathInputEdit.text()
    #     out_path = self.filePathOutEdit.text()
    #
    #     if input_path == "":
    #         QMessageBox.warning(self, '警告', '路径为空')
    #
    #     self.renameFile(input_path, out_path)


    # def renameFile(self,src_dir,dis_dir):
    #     try:
    #         dirs_list = [src_dir]  # 建立一个列表存放该文件夹及包含的所有嵌套及多重嵌套的子文件夹名
    #         for root, dirs, flies in os.walk(src_dir, topdown=False):  # 输出目录树中的根目录，文件夹名，文件名
    #             for name in dirs:
    #                 if (name != []):  # 去除无效目录
    #                     dirs_list.append(os.path.join(root, name))  # 循环加入所有嵌套及多重嵌套的带路径子文件夹名
    #         os.chdir(src_dir)  # 切换OS工作目录到文件所在位置
    #
    #         for each_dirs in dirs_list:  # 遍历所有文件夹
    #             files_list = os.listdir(each_dirs)  # 生成待改名文件列表
    #             os.chdir(each_dirs)  # 切换OS工作目录到文件所在位置
    #             for each_object in files_list:
    #
    #                 if os.path.isfile(each_object):  # 判断该对象是否为文件
    #                     curPathName = os.getcwd().split('\\')[-1]  # 取路径的最后一级文件夹
    #                     fext = os.path.splitext(each_object)[1]  # 分离文件拓展名,取扩展名
    #                     os.rename(each_object, "{}{}".format(curPathName, fext))  # 用最后一级文件夹名给文件重命名 ,报错时检查是否同类型文件有多个
    #                     self.logTextEdit.append("%s 重复名成功" % each_object)
    #
    #                 else:  # 不是文件则跳过
    #                     continue
    #
    #     except Exception as e:
    #         self.logTextEdit.append("%s " % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = CopyFile()
    rcp.setWindowTitle("Copy File")
    rcp.show()
    sys.exit(app.exec_())







