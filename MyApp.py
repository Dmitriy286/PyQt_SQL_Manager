from PySide2 import QtWidgets, QtCore, QtSql, QtGui
from Form import Ui_MainWindow as ui


class MyApp(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        self.ui.setupUi()
        # self.initThreads()


