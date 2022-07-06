from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql
from PySide2.QtGui import QStandardItem, Qt
from PySide2.QtSql import QSqlTableModel
from sqlalchemy import column
from sqlalchemy.engine import row

from Form import Ui_MainWindow
from Model import init_db, Employee, del_db, commit_session
from Controller import show_all_employees, delete_employee, query_find_employee_by_id, changeEmployee



class MyApp(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        # del_db()
        init_db()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadEmployeesTable()

        self.initSignals()
        # self.initThreads()

    def initSignals(self):
        # self.ui.openDelegate.textEdited.connect(self.getDataFromCell)
        self.ui.openDelegate.textEdited.connect(self.onChanged)
        # self.ui.openDelegate.textChanged[str].connect(self.onChanged)
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        self.ui.savePB.clicked.connect(self.onSavePBClicked)

    def onChanged(self, text):
        print("onChanged")
        print(text)
        print(str(text))
        # print(self.ui.openDelegate.getModelData())
        # print(self.ui.openDelegate.createEditor().text)
        # property("text")
        # self.ui.mainTableView.clicked.connect(self.write_text)
        # self.ui.mainTableView.installEventFilter(self)

    # def write_text(self, index):
    #     row, column, cell_value = index.row(), index.column(), index.data()
    #     print("Row {}, Column {} clicked - value: {}".format(row, column, cell_value))
    #     self.ui.lineEdit.setText("%s" % cell_value)
    #     self.ui.mainTableView.close()
    #
    # def eventFilter(self, obj, event):
    #     if obj is self.ui.mainTableView and event.type() == QtCore.QEvent.KeyPress:
    #         if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
    #             indexes = self.ui.mainTableView.selectedIndexes()
    #             if indexes:
    #                 self.write_text(indexes[0])
    #     return super(MyApp, self).eventFilter(obj, event)

    # def submit(self):
    #     self.model.database().transaction()
    #     self.model.submitAll()
    #     self.model.database().commit()

    # def setDataToCell(self, selected_cell):
    #     row = selected_cell.row()
    #     column = selected_cell.column()
    #     item = QStandardItem(self.model.item(row, column).text())
    #     self.model.setItem(row, column, item)

    def getDataFromCell(self, selected_cell):
        row = selected_cell.row()
        column = selected_cell.column()
        text = self.model.item(row, column).text()
        id = int(text)
        print(id)
        model = self.ui.mainTableView.model()
        # commit_session()

    def loadEmployeesTable(self):
        headers = ["id", "name", "username", "password", "orders"]
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        data = show_all_employees()
        model.setRowCount(len(data))

        for row, employee in enumerate(data):
            if employee["orders"] == None:
                o = "-"
            else:
                o = str([id for id in employee["orders"]])
            model.setItem(row, 0, QtGui.QStandardItem(str(employee["id"]))) # todo не выводит id в таблице
            model.setItem(row, 1, QtGui.QStandardItem(employee["name"]))
            model.setItem(row, 2, QtGui.QStandardItem(employee["username"]))
            model.setItem(row, 3, QtGui.QStandardItem(employee["password"]))
            model.setItem(row, 4, QtGui.QStandardItem(o))

        self.ui.mainTableView.setModel(model)

        self.ui.mainTableView.setItemDelegateForColumn(1, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(2, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(3, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(4, self.ui.openDelegate)

        self.ui.mainTableView.horizontalHeader().setSectionsMovable(True)
        self.ui.mainTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.lcdNumber.display(model.rowCount())

        model.dataChanged.connect(self.mainTableViewDataChanged)

    def mainTableViewDataChanged(self, item):
        model = self.ui.mainTableView.model()
        print(item.data(0))
        id_= model.index(item.row(), 0)
        employee_id = int(id_.data(0))
        employee = query_find_employee_by_id(employee_id)
        employee.name = item.data(0)
        commit_session()


    def onSavePBClicked(self):
        print("Save button is working")
        model = self.ui.mainTableView.model()
        index = model.rowCount()
        # model = self.ui.mainTableView.model()
        # model.setData(model.index(index, 1), self.ui.mainTableView.currentIndex())
        # self.model.setData(self.model.index(index, 2), self.ui.lineEdit_2.text())
        self.saveDataInNewRow(self, index)
        # self.model.submit()
        # commit_session()

    def onAddRowPBClicked(self):
        model = self.ui.mainTableView.model()
        index = model.rowCount()
        model.insertRows(index, 1)

        # model.setData(model.index(index, 1), model.index(index, 1).data(0))
        # model.setData(model.index(index, 2), model.index(index, 2).data(0))
        # model.setData(model.index(index, 3), model.index(index, 3).data(0))
        # model.setData(model.index(index, 4), model.index(index, 4).data(0))
    def saveDataInNewRow(self, index):
        model = self.ui.mainTableView.model()
        model.setData(model.index(index, 1), "test1")
        model.setData(model.index(index, 2), "test2")
        model.setData(model.index(index, 3), "test3")
        model.setData(model.index(index, 4), "[]")
        model.submitAll()

        commit_session()
        print("Adding method is working")
        self.ui.lcdNumber.display(model.rowCount())

    def onDeleteRowPBClicked(self):
        model = self.ui.mainTableView.model()
        if self.ui.mainTableView.currentIndex().row() > -1:
            row_index = self.ui.mainTableView.currentIndex().row()
            txt = self.model.takeItem(self.ui.mainTableView.currentIndex().row(), 0).text()
            id = int(txt)
            model.removeRow(row_index)
            delete_employee(id)
            self.ui.lcdNumber.display(model.rowCount())
        else:
            QtWidgets.QMessageBox.question(self, 'Message', "Please select a row would you like to delete", QtWidgets.QMessageBox.Ok)

        commit_session()

        print("Delete method works")
        self.ui.lcdNumber.display(model.rowCount())



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


