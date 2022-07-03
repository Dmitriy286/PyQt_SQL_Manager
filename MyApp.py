from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql

from Form import Ui_MainWindow as ui
from Model import Employee



class MyApp(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        self.ui.setupUi()
        # self.initThreads()

    def initSignals(self):

        self.ui.mainTableView
        pb.clicked.connect(self.addNewUser)





if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


