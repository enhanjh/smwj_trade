# python 3.6 32bit
# installed package
# 1. win32com(pywin32)
# 2. pyqt5


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.statusBar().showMessage(self.kiwoom.dynamicCall("CommConnect()"))
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")