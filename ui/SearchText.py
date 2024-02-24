#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 14:00
# @Author  : nqp
# @File    : SearchText.py
# @Description : 关键字搜索
import sys
import threading
import time
from pathlib import Path

import qdarkstyle
from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QFileDialog, \
    QMessageBox, QApplication


class SearchText(QWidget):
    def __init__(self):
        super(SearchText, self).__init__()
        self.resize(700, 500)
        self.setWindowTitle("关键字搜索")
        self.setUpUI()

    def setUpUI(self):
        self.mainLayout = QVBoxLayout()  # 垂直布局
        self.Hlayout1 = QHBoxLayout()  # 水平布局
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        self.search_path_edit = QLineEdit()
        self.search_path_edit.setFixedHeight(32)
        self.search_path_edit.setPlaceholderText("搜索根目录")
        self.search_path_edit.setFont(font)

        self.inputDirBtn = QPushButton("选择")
        self.inputDirBtn.setObjectName("inputDirBtn")
        self.inputDirBtn.setFixedHeight(32)
        self.inputDirBtn.setFixedWidth(100)
        self.inputDirBtn.setFont(font)

        self.search_text_edit = QLineEdit()
        self.search_text_edit.setFixedHeight(32)
        self.search_text_edit.setPlaceholderText("搜索关键字")
        self.search_text_edit.setFont(font)

        self.search_Btn = QPushButton("搜索")
        self.search_Btn.setObjectName("search_Btn")
        self.search_Btn.setFixedHeight(32)
        self.search_Btn.setFixedWidth(100)
        self.search_Btn.setFont(font)


        self.clearBtn = QPushButton("清除记录")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFont(font)

        # 打印日志
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setObjectName("logTextEdit")

        self.Hlayout1.addWidget(self.search_path_edit)
        self.Hlayout1.addWidget(self.inputDirBtn)
        self.Hlayout2.addWidget(self.search_text_edit)
        self.Hlayout2.addWidget(self.search_Btn)
        self.Hlayout3.addWidget(self.clearBtn)
        self.Hlayout4.addWidget(self.logTextEdit)

        self.mainLayout.addLayout(self.Hlayout1)
        self.mainLayout.addLayout(self.Hlayout2)
        self.mainLayout.addLayout(self.Hlayout3)
        self.mainLayout.addLayout(self.Hlayout4)

        self.setLayout(self.mainLayout)

        QMetaObject.connectSlotsByName(self)
##########################按钮事件###################################
    @pyqtSlot()
    def on_clearBtn_clicked(self):
        self.logTextEdit.clear()

    @pyqtSlot()
    def on_inputDirBtn_clicked(self):
        filePath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.search_path_edit.setText(filePath)

    @pyqtSlot()
    def on_search_Btn_clicked(self):
        search_path = self.search_path_edit.text().strip()
        search_text = self.search_text_edit.text().strip()

        if search_text =="" or search_path =="":
            QMessageBox.warning(self, '警告', '搜索路径或关键字不能为空！')
            return

        if not Path(search_path).exists():
            QMessageBox.warning(self, '警告', '搜索路径不存在！')
            return

        # 清空日志
        self.logTextEdit.clear()
        self.thread = threading.Thread(target=self.searchTagText,
                                       args=(search_path,search_text))
        # 守护线程随sys.exit(0)退出而退出(默认非守护线程会阻塞主程序退出)
        self.thread.daemon = True
        self.thread.start()

########################数据处理函数###################################
    def searchTagText(self,searchPath,searchText):
        count = 0
        arr = []
        byte_tag = bytes(searchText, encoding="utf8")
        for file in Path(searchPath).rglob(f"*"):
            if file.is_file():
                count += 1
                line_num = 0
                self.print_msg('searching->{}'.format(file.name))
                try:
                    with open(str(file),"rb") as f:
                        lines = f.readlines()
                        for line in lines:
                            line_num += 1
                            if byte_tag in line:
                                arr.append('{}->line:{}'.format(file.name, line_num))
                                break


                except BaseException as e1:
                    self.print_msg('file:{} had exception:{}'.format(file.name, e1))
                finally:
                    f.close()
        self.print_msg('These files had {} contains "{}":'.format(len(arr), searchText))
        self.print_msg('search count ->{}'.format(count))
        for f in arr:
            self.print_msg(f)
        del arr[:]

    def print_msg(self, msg):
            time.sleep(0.02)
            self.logTextEdit.append(msg)
            self.logTextEdit.ensureCursorVisible()  # 每次添加文本光标都在最后一行
            self.logTextEdit.moveCursor(self.logTextEdit.textCursor().End)  # 文本框显示到底部


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    rcp = SearchText()
    rcp.show()
    sys.exit(app.exec_())
