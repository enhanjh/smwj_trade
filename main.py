import sys
import kiwoom.api as kw


if __name__ == "__main__":
    app = kw.QApplication(sys.argv)
    myWindow = kw.MyWindow()
    myWindow.show()
    app.exec_()