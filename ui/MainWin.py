import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import qdarkstyle
import sip
from ui.RenameFile import RenameFile
from ui.ImageAlign import ImageAlign
from ui.FileConversion import ChangeFile
from ui.CopyFile import CopyFile
from ui.SearchText import SearchText
from ui.ImageCut import ImageCut
from ui.GetImageXY import GetImageXY
from ui.ImageClassifiaction import ImageClassifiaction


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.resize(900, 600)
        self.setWindowTitle("Test 工具")
        self.setUpUI()

    def setUpUI(self):
        self.hboxMainLayout = QHBoxLayout()  # 水平布局
        # self.buttonlayout = QVBoxLayout()  #垂直布局

        font = QFont()
        font.setPixelSize(13)

        bar = self.menuBar()
        self.fileMenu = bar.addMenu("文件处理")
        self.imageMenu = bar.addMenu("图像处理")

        self.copy_menu = QAction("复制文件", self)
        self.changfile_menu = QAction("文件转换",self)
        self.renamefile_menu = QAction("重命名文件",self)
        self.search_text_menu = QAction("搜索关键字",self)



        self.image_fusion_menu = QAction("图像对齐",self)
        self.image_color_menu = QAction("图像色彩转换",self)
        self.image_cut_menu = QAction("图片裁切")
        self.image_xy_menu = QAction("图片坐标获取",self)
        self.imgClassifiaction_menu = QAction("图片分类", self)


        self.imageMenu.addAction(self.image_fusion_menu)
        self.imageMenu.addAction(self.image_color_menu)
        self.imageMenu.addAction(self.image_cut_menu)
        self.imageMenu.addAction(self.image_xy_menu)
        self.imageMenu.addAction(self.imgClassifiaction_menu)

        self.fileMenu.addAction(self.copy_menu)
        self.fileMenu.addAction(self.changfile_menu)
        self.fileMenu.addAction(self.renamefile_menu)
        self.fileMenu.addAction(self.search_text_menu)


        # self.imageMenu.addAction()

        # self.signUpAction = QAction("", self)
        # self.changePasswordAction = QAction("修改密码", self)
        # self.signInAction = QAction("登录", self)
        # self.quitSignInAction = QAction("退出登录", self)
        # self.quitAction = QAction("退出", self)

        self.tooBar = QToolBar()
        self.tooBar.setObjectName("tooBar")
        self.imgRongHeAction = QAction("图像对齐", self)
        self.imgRongHeAction.setFont(font)
        self.tooBar.addAction(self.imgRongHeAction)

        self.copyFileAction = QAction("复制文件",self)
        self.copyFileAction.setFont(font)
        self.tooBar.addAction(self.copyFileAction)

        self.renameFileAction = QAction("重命名文件",self)
        self.renameFileAction.setFont(font)
        self.tooBar.addAction(self.renameFileAction)

        self.changeFileAction = QAction("文件转换",self)
        self.changeFileAction.setFont(font)
        self.tooBar.addAction(self.changeFileAction)

        self.imgCutAction = QAction("图片裁切",self)
        self.imgCutAction.setFont(font)
        self.tooBar.addAction(self.imgCutAction)

        self.imgGetXYAction = QAction("图片坐标获取",self)
        self.imgGetXYAction.setFont(font)
        self.tooBar.addAction(self.imgGetXYAction)

        self.searchTextAction = QAction("关键字搜索",self)
        self.searchTextAction.setFont(font)
        self.tooBar.addAction(self.searchTextAction)

        self.imgClassifiAction = QAction("图片分类", self)
        self.imgClassifiAction.setFont(font)
        self.tooBar.addAction(self.imgClassifiAction)


        self.addToolBar(self.tooBar)

        ###################菜单栏事件#############################
        self.copy_menu.triggered.connect(self.showCopyFileWin)
        self.renamefile_menu.triggered.connect(self.showRenameFileWin)
        self.changfile_menu.triggered.connect(self.showChangeFileWin)
        self.search_text_menu.triggered.connect(self.showSearchTextWin)

        self.image_fusion_menu.triggered.connect(self.showImgRongHeWin)
        self.image_cut_menu.triggered.connect(self.showImgCutWin)
        self.image_xy_menu.triggered.connect(self.showGetImgXYWin)


        ###################工具栏事件############################
        self.imgRongHeAction.triggered.connect(self.showImgRongHeWin)
        self.copyFileAction.triggered.connect(self.showCopyFileWin)
        self.renameFileAction.triggered.connect(self.showRenameFileWin)
        self.changeFileAction.triggered.connect(self.showChangeFileWin)
        self.imgRongHeAction.triggered.connect(self.showImgRongHeWin)
        self.imgCutAction.triggered.connect(self.showImgCutWin)
        self.searchTextAction.triggered.connect(self.showSearchTextWin)
        self.imgGetXYAction.triggered.connect(self.showGetImgXYWin)




        # self.Menu.addAction(self.signUpAction)
        # self.Menu.addAction(self.changePasswordAction)
        # self.Menu.addAction(self.signInAction)
        # self.Menu.addAction(self.quitSignInAction)
        # self.Menu.addAction(self.quitAction)
        #
        # self.signUpAction.setEnabled(True)
        # self.changePasswordAction.setEnabled(True)
        # self.signInAction.setEnabled(False)
        # self.quitSignInAction.setEnabled(False)
        # self.widget.is_student_signal.connect(self.studentSignIn)
        # self.Menu.triggered[QAction].connect(self.menuTriggered)

        # self.quitAction.triggered.connect(qApp.quit)

######################界面显示函数###########################################

    #获取图片坐标
    def showGetImgXYWin(self):
        self.imgXY = GetImageXY()
        self.setCentralWidget(self.imgXY)
        self.setWindowTitle("Test 工具 ---获取图片坐标")


    #图片裁切
    def showImgCutWin(self):
        self.imgCutWin = ImageCut()
        self.setCentralWidget(self.imgCutWin)
        self.setWindowTitle("Test 工具 ---图片裁切")

    #图像融合窗口
    def showImgRongHeWin(self):
        self.image_align_win = ImageAlign()
        self.setCentralWidget(self.image_align_win)
        self.setWindowTitle("Test 工具 ---图像对齐")


    #显示复制文件窗口
    def showCopyFileWin(self):
        self.copyFileWin = CopyFile()
        self.setCentralWidget(self.copyFileWin)
        self.setWindowTitle("Test 工具 ---复制文件")

    #显示重命名窗口
    def showRenameFileWin(self):
        self.renameFileWin = RenameFile()
        self.setCentralWidget(self.renameFileWin)
        self.setWindowTitle("Test 工具 ---重命名文件")

    #显示文件转换窗口
    def showChangeFileWin(self):
        self.changeFileWin = ChangeFile()
        self.setCentralWidget(self.changeFileWin)
        self.setWindowTitle("Test 工具 ---文件转换")
    #关键字查找
    def showSearchTextWin(self):
        self.SearchTextWin = SearchText()
        self.setCentralWidget(self.SearchTextWin)
        self.setWindowTitle("Test 工具 ---关键字搜索")

    #图片分类(黑屏、椒盐噪声)
    def showImgClassifiaction(self):
        self.imgClassifiactonWin = ImageClassifiaction()
        self.setCentralWidget(self.imgClassifiAction)
        self.setWindowTitle("Test 工具 ---图片分类")


    def studentSignIn(self,userId,userName):
        pass
        # sip.delete(self.widget)
        # self.widget = AdminHome(userId,userName)
        # self.setCentralWidget(self.widget)
        # self.changePasswordAction.setEnabled(False)
        # self.signUpAction.setEnabled(True)
        # self.signInAction.setEnabled(False)
        # self.quitSignInAction.setEnabled(True)

    def menuTriggered(self, q):

        if(q.text()==""):
            pass
            # changePsdDialog=changePasswordDialog(self)
            # changePsdDialog.show()
            # changePsdDialog.exec_()
        if (q.text() == "注册"):
            pass
            # sip.delete(self.widget)
            # self.widget = SignUpWidget()
            # self.setCentralWidget(self.widget)
            # self.widget.student_signup_signal[str].connect(self.studentSignIn)
            # self.signUpAction.setEnabled(False)
            # self.changePasswordAction.setEnabled(True)
            # self.signInAction.setEnabled(True)
            # self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出登录"):
            pass
            # sip.delete(self.widget)
            # self.widget = SignInWidget()
            # self.setCentralWidget(self.widget)
            # self.widget.is_admin_signal.connect(self.adminSignIn)
            # self.widget.is_student_signal[str].connect(self.studentSignIn)
            # self.signUpAction.setEnabled(True)
            # self.changePasswordAction.setEnabled(True)
            # self.signInAction.setEnabled(False)
            # self.quitSignInAction.setEnabled(False)
        if (q.text() == "登录"):
            pass
            # print("登录*****")
            # sip.delete(self.widget)
            # self.widget = SignInWidget()
            # self.setCentralWidget(self.widget)
            # self.widget.is_admin_signal.connect(self.adminSignIn)
            # self.widget.is_student_signal[str].connect(self.studentSignIn)
            # self.signUpAction.setEnabled(True)
            # self.changePasswordAction.setEnabled(True)
            # self.signInAction.setEnabled(False)
            # self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出"):
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv) #qdarkstyle.load_stylesheet_pyqt5()
    # app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
