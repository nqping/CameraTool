#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 10:33
# @Author  : nqp
# @File    : RenameFile.py
# @Description : raw深度图文件转换成16位png图
import shutil
import sys,os
import threading
import time
from pathlib import PurePath, Path

import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QApplication,QTextEdit,QMessageBox,QGroupBox,QTextBrowser,QLabel



class RenameFile(QWidget):

    def __init__(self):
        super(RenameFile,self).__init__()
        self.resize(700, 500)
        self.setUpUI()


    def setUpUI(self):
        self.layout = QVBoxLayout()  #垂直布局
        self.Hlayout1 = QHBoxLayout()  #水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        # self.groupbox1 = QGroupBox("路径最后-级文件夹名重命名单个文件",self)

        font = QFont()
        font.setPixelSize(15)

        # Hlayout1控件的初始化
        self.filePathInputEdit = QLineEdit()
        self.filePathInputEdit.setFixedHeight(32)
        self.filePathInputEdit.setPlaceholderText("目标路径")
        self.filePathInputEdit.setFont(font)

        # self.filePathOutEdit = QLineEdit()
        # self.filePathOutEdit.setFixedHeight(32)
        # self.filePathOutEdit.setPlaceholderText("输出目录")
        # self.filePathOutEdit.setFont(font)

        self.inputDirBtn = QPushButton("选择目录")
        self.inputDirBtn.setObjectName("inputDirBtn")
        self.inputDirBtn.setFixedHeight(32)
        self.inputDirBtn.setFont(font)

        # self.outDirBtn = QPushButton("选择输出目录")
        # self.outDirBtn.setObjectName("outDirBtn")
        # self.outDirBtn.setFixedHeight(32)
        # self.outDirBtn.setFont(font)

        self.fist_name_label = QLabel("自定义前缀")
        self.fist_name_label.setFont(font)
        self.fist_name_label.setFixedHeight(32)

        self.fileformatEdit = QLineEdit()
        self.fileformatEdit.setObjectName("fileformatEdit")
        self.fileformatEdit.setPlaceholderText("自定义前缀+数字,如AS59_1,默认从1开始,为空时取最后一级目录名")
        self.fileformatEdit.setFixedHeight(32)
        self.fileformatEdit.setFont(font)


        self.renameBtn = QPushButton("重命名")
        self.renameBtn.setObjectName("renameBtn")
        self.renameBtn.setFixedHeight(32)
        self.renameBtn.setFont(font)

        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        self.logTextEdit = QTextBrowser()
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setPlaceholderText("Pring log ...")

        self.Hlayout1.addWidget(self.filePathInputEdit)
        self.Hlayout1.addWidget(self.inputDirBtn)
        # self.Hlayout2.addWidget(self.fist_name_label)
        self.Hlayout2.addWidget(self.fileformatEdit)

        self.Hlayout3.addWidget(self.renameBtn)

        self.Hlayout3.addWidget(self.clearBtn)
        self.Hlayout4.addWidget(self.logTextEdit)

        # Hlayout2初始化
        self.layout.addLayout(self.Hlayout1)
        self.layout.addLayout(self.Hlayout2)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout4)

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
    def on_renameBtn_clicked(self):
        input_path = self.filePathInputEdit.text()
        # out_path = self.filePathOutEdit.text()
        first_name = self.fileformatEdit.text()

        if input_path == "":
            QMessageBox.warning(self, '警告', '路径为空')
            return

        self.thread = threading.Thread(target=self.renameFile, args=(input_path, first_name))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

        # self.renameFile(input_path,first_name)

    def print_msg(self,msg):
        time.sleep(0.02)
        self.logTextEdit.append(msg)
        self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
        self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部

    def renameFile(self,src_dir,first_name):
        if first_name =="":
            if os.path.exists(src_dir):  # 判断该路径是否真实存在
                dirs_list = [src_dir]  # 建立一个列表存放该文件夹及包含的所有嵌套及多重嵌套的子文件夹名

                for root, dirs, flies in os.walk(src_dir, topdown=False):  # 输出目录树中的根目录，文件夹名，文件名
                    for name in dirs:
                        if (name != []):  # 去除无效目录
                            dirs_list.append(os.path.join(root, name))  # 循环加入所有嵌套及多重嵌套的带路径子文件夹名

                os.chdir(src_dir)  # 切换OS工作目录到文件所在位置

                num = 0
                for each_dirs in dirs_list:  # 遍历所有文件夹
                    files_list = os.listdir(each_dirs)  # 生成待改名文件列表
                    os.chdir(each_dirs)  # 切换OS工作目录到文件所在位置
                    num = 1
                    for each_object in files_list:
                        if os.path.isfile(each_object):  # 判断该对象是否为文件
                            curPathName = os.getcwd().split('\\')[-1]  # 取路径的最后一级文件夹
                            fext = os.path.splitext(each_object)[1]  # 分离文件拓展名,取扩展名
                            os.rename(each_object,
                                      "{}_{}{}".format(curPathName, num, fext))  # 用最后一级文件夹名给文件重命名 ,报错时检查是否同类型文件有多个
                            num += 1  # 操作次数加一
                            # print("%s rename OK" % each_object)
                            self.print_msg("{} rename OK".format(each_object))

                        else:  # 不是文件则跳过
                            continue

            # count = 1
            # for file in Path(src_dir).glob(f"*"):
            #
            #     if file.is_file():
            #         first_name = str(file.parent).split("\\")[-1]  #取上一级目录名
            #         new_file = Path.joinpath(file.parent, first_name + "_" + str(count) + file.suffix)
            #         os.rename(file, new_file)  # 用最后一级文件夹名给文件重命名 ,报错时检查是否同类型文件有多个
            #         # print("{} 重命名成功".format(file))
            #         self.print_msg("{} 重命名成功".format(file))
            #         count += 1
            #     else:
            #         count = 0

        else:
            count = 1
            for file in Path(src_dir).rglob(f"*"):

                if file.is_file():
                    new_file = Path.joinpath(file.parent, first_name + "_" + str(count) + file.suffix)
                    os.rename(file, new_file)  # 用最后一级文件夹名给文件重命名 ,报错时检查是否同类型文件有多个
                    # print("{} 重命名成功".format(file))
                    self.print_msg("{} 重命名成功".format(file))
                    count += 1
                else:
                    count = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = RenameFile()
    rcp.setWindowTitle("444444")
    rcp.show()
    sys.exit(app.exec_())







