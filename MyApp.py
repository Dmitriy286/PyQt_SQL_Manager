from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql
from PySide2.QtGui import QStandardItem, Qt
from PySide2.QtSql import QSqlTableModel
from sqlalchemy import column
from sqlalchemy.engine import row

from Form import Ui_MainWindow
from Model import init_db, Employee, del_db, commit_session
from Controller import show_all_employees, delete_employee, query_find_employee_by_id, \
    changeEmployee, create_employee, add_employee



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
        self.temp_employee = create_employee()


    def initSignals(self):
        # self.ui.openDelegate.textEdited.connect(self.getDataFromCell)
        # self.ui.openDelegate.textEdited.connect(self.onChanged)
        # self.ui.openDelegate.textChanged[str].connect(self.onChanged)
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        self.ui.savePB.clicked.connect(self.onSavePBClicked)
        self.ui.showAllPB.clicked.connect(self.onShowAllPBClicked)

    def onShowAllPBClicked(self) -> None:
        self.loadEmployeesTable()

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

        self.ui.mainTableView.horizontalHeader().setSectionsMovable(True)
        self.ui.mainTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.lcdNumber.display(model.rowCount())

        model.dataChanged.connect(self.mainTableViewDataChanged)

    def mainTableViewDataChanged(self, item):
        model = self.ui.mainTableView.model()
        print(item.data(0))
        id_= model.index(item.row(), 0)
        if id_.data(0) != None:
            employee_id = int(id_.data(0))
            employee = query_find_employee_by_id(employee_id)
            if item.column() == 1:
                employee.name = item.data(0)
            if item.column() == 2:
                employee.username = item.data(0)
            if item.column() == 3:
                employee.password = item.data(0)

        else:
            if item.column() == 1:
                model.setData(model.index(item.row(), item.column()), item.data(0))
                self.temp_employee["name"] = model.index(item.row(), item.column()), item.data(0)
            if item.column() == 2:
                model.setData(model.index(item.row(), item.column()), item.data(0))
                self.temp_employee["username"] = model.index(item.row(), item.column()), item.data(0)
            if item.column() == 3:
                model.setData(model.index(item.row(), item.column()), item.data(0))
                self.temp_employee["password"] = model.index(item.row(), item.column()), item.data(0)

            # model.submit()

            print("Данные из ячейки в модели:")
            print(model.index(item.row(), item.column()).data(0))

            print("Данные из всех ячеек в модели:")
            print(model.index(item.row(), 1).data(0))
            print(model.index(item.row(), 2).data(0))
            print(model.index(item.row(), 3).data(0))

            print("Данные из полей временного employee:")
            print(self.temp_employee["name"][1])
            print(type(self.temp_employee["name"][1]))
            print(self.temp_employee["username"][1])
            print(self.temp_employee["password"][1])


    def onSavePBClicked(self):
        model = self.ui.mainTableView.model()
        index = model.rowCount()
        if model.item(index, 0) != None:
            print("Save button is working. Change is saving")
            commit_session()
        else:
            print("Save button is working. New row is saving")
            model = self.ui.mainTableView.model()
            index = model.rowCount()
            self.saveDataInNewRow(index)

    def onAddRowPBClicked(self):
        model = self.ui.mainTableView.model()
        index = model.rowCount()
        model.insertRows(index, 1)

    def saveDataInNewRow(self, i):
        new_employee = add_employee()
        model = self.ui.mainTableView.model()

        print("Данные из полей временного employee в сейвметоде:")
        print(self.temp_employee["name"][1])
        print(self.temp_employee["username"][1])
        print(self.temp_employee["password"][1])

        new_employee.name = self.temp_employee["name"][1]
        new_employee.username = self.temp_employee["username"][1]
        new_employee.password = self.temp_employee["password"][1]
        self.temp_employee["name"] = ""
        self.temp_employee["username"] = ""
        self.temp_employee["password"] = ""
        print(new_employee.name)

        commit_session()
        print("Adding method is working")
        self.ui.lcdNumber.display(model.rowCount())
        self.loadEmployeesTable()

    def onDeleteRowPBClicked(self):
        model = self.ui.mainTableView.model()
        if self.ui.mainTableView.currentIndex().row() > -1:
            row_index = self.ui.mainTableView.currentIndex().row()
            txt = model.takeItem(self.ui.mainTableView.currentIndex().row(), 0).text()
            id = int(txt)
            model.removeRow(row_index)
            delete_employee(id)
            self.ui.lcdNumber.display(model.rowCount())
        else:
            QtWidgets.QMessageBox.question(self, 'Message', "Please select a row to delete", QtWidgets.QMessageBox.Ok)

        commit_session()

        print("Delete method works")
        self.ui.lcdNumber.display(model.rowCount())



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


