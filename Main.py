#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/22 15:46
# @Author  : nqp
# @File    : MainWin.py
# @Description : 程序入口

import sys

import qdarkstyle
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ui.MainWin import Main


if __name__ == "__main__":
    app = QApplication(sys.argv) #qdarkstyle.load_stylesheet_pyqt5()
    app.setWindowIcon(QIcon("../images/xe.ico"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
