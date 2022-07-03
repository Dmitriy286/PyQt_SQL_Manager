from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql
from PySide2.QtGui import QStandardItem
from sqlalchemy import column
from sqlalchemy.engine import row

from Form import Ui_MainWindow
from Model import init_db, Employee, del_db, commit_session
from Controller import show_all_employees, delete_employee, query_find_employee_by_id



class MyApp(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        # del_db()
        init_db()


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadEmployeesTable()

        self.initSignals()
        # self.ui.openDelegate.textEdited.connect(self.setDataToCell)
        # self.ui.openDelegate.textEdited.connect(self.getDataFromCell)
        self.ui.openDelegate.textEdited.connect(self.getDataFromCell)
        # self.ui.openDelegate.selectionChanged.connect(self.getDataFromCell)



    def initSignals(self):
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        # self.ui.mainTableView
        # pb.clicked.connect(self.addNewUser)

    # self.initThreads()

    # def setDataToCell(self, selected_cell):
    #     row = selected_cell.row()
    #     column = selected_cell.column()
    #     item = QStandardItem(self.model.item(row, column).text())
    #     self.model.setItem(row, column, item)


    def getDataFromCell(self, selected_cell):
        row = selected_cell.row()
        column = selected_cell.column()

        txt = self.model.item(row, 0).text()
        id = int(txt)

        employee = query_find_employee_by_id(id)

        model = self.ui.mainTableView.model()

        model.setData(model.index(row, column), "Bob")
        print(f"{employee.name}")
        # item = QStandardItem(f"{self.ui.openDelegate.text()}")
        # self.model.setItem(row, column, item)
        text = self.model.item(row, column).text()
        print(text)
        self.ui.openDelegate.dumpObjectInfo()
        commit_session()
        text = self.model.item(row, column).text()
        print(text)

    def loadEmployeesTable(self):
        headers = ["id", "name", "username", "password", "orders"]
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(headers)

        data = show_all_employees()

        self.model.setRowCount(len(data))

        for row, employee in enumerate(data):
            if employee["orders"] == None:
                o = "-"
            else:
                o = str([id for id in employee["orders"]])
            self.model.setItem(row, 0, QtGui.QStandardItem(str(employee["id"]))) # todo не выводит id в таблице
            self.model.setItem(row, 1, QtGui.QStandardItem(employee["name"]))
            self.model.setItem(row, 2, QtGui.QStandardItem(employee["username"]))
            self.model.setItem(row, 3, QtGui.QStandardItem(employee["password"]))
            self.model.setItem(row, 4, QtGui.QStandardItem(o))

        self.ui.mainTableView.setModel(self.model)
        self.ui.mainTableView.setItemDelegateForColumn(1, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(2, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(3, self.ui.openDelegate)
        self.ui.mainTableView.setItemDelegateForColumn(4, self.ui.openDelegate)
        # self.ui.mainTableView.setItemDelegateForColumn(1, line)

        self.ui.lcdNumber.display(self.model.rowCount())

        self.ui.mainTableView.horizontalHeader().setSectionsMovable(True)
        self.ui.mainTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def onAddRowPBClicked(self):
        index = self.model.rowCount()
        self.model.insertRows(index, 1)
        # self.model.setData(self.model.index(index, 1), self.ui.lineEdit.text())
        # self.model.setData(self.model.index(index, 2), self.ui.lineEdit_2.text())
        # self.model.setData(self.model.index(index, 4), self.ui.lineEdit_3.text())
        # self.model.setData(self.model.index(index, 3), self.ui.dateEdit.text())
        # self.model.submitAll()

        commit_session()
        print("Adding method works")
        self.ui.lcdNumber.display(self.model.rowCount())

    def onDeleteRowPBClicked(self):

        if self.ui.mainTableView.currentIndex().row() > -1:
            row_index = self.ui.mainTableView.currentIndex().row()
            txt = self.model.takeItem(self.ui.mainTableView.currentIndex().row(), 0).text()
            id = int(txt)
            self.model.removeRow(row_index)
            delete_employee(id)
            self.ui.lcdNumber.display(self.model.rowCount())
        else:
            QtWidgets.QMessageBox.question(self, 'Message', "Please select a row would you like to delete", QtWidgets.QMessageBox.Ok)

        commit_session()
        print("Delete method works")
        self.ui.lcdNumber.display(self.model.rowCount())





if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


