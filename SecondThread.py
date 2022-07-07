from PySide2 import QtCore, QtGui, QtWidgets

from Form import Ui_MainWindow
from Controller import show_all


class SecondaryTable(QtCore.QThread):
    mysignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(SecondaryTable, self).__init__(parent)
        self.entity = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def run(self):
        self.status = True
        model = QtGui.QStandardItemModel()
        self.ui.secondaryTableView.setModel(model)
        # self.entity = globals()[self.ui.comboBox.currentText()]
        while self.status:
            headers = ['id', 'name']

            model.setHorizontalHeaderLabels(headers)

            data = show_all(self.entity)
            model.setRowCount(len(data))

            for row, obj in enumerate(data):
                model.setItem(row, 0, QtGui.QStandardItem(obj["id"]))
                model.setItem(row, 1, QtGui.QStandardItem(obj["name"]))

            self.ui.secondaryTableView.horizontalHeader().setSectionsMovable(True)
            self.ui.secondaryTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

            self.mysignal.emit(str(model.rowCount()))