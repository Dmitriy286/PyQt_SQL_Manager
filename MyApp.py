from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql

from Form import Ui_MainWindow as ui



class MyApp(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        self.ui.setupUi()
        # self.initThreads()





if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


