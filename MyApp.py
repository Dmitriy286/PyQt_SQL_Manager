from typing import List

from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql
from PySide2.QtGui import QStandardItem, Qt
from PySide2.QtSql import QSqlTableModel
from sqlalchemy import column
from sqlalchemy.engine import row

from Form import Ui_MainWindow
from Model import init_db, Employee, Customer, Order, del_db, commit_session
from Controller import delete_obj, \
    create_obj, add_obj, show_all, query_find_by_id


class MyApp(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        # del_db()
        init_db()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entity = None
        self.loadMainTable()

        self.initSignals()
        # self.initThreads()
        # self.temp_obj = create_obj()
        self.temp_obj = {}


    def initSignals(self):
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        self.ui.savePB.clicked.connect(self.onSavePBClicked)
        self.ui.showAllPB.clicked.connect(self.onShowAllPBClicked)
        self.ui.comboBox.currentTextChanged.connect(self.loadMainTable)

    def onShowAllPBClicked(self) -> None:
        self.loadMainTable(self.entity)

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

    def getDataFromCell(self, selected_cell):
        row = selected_cell.row()
        column = selected_cell.column()
        text = self.model.item(row, column).text()
        id = int(text)
        print(id)
        model = self.ui.mainTableView.model()
        # commit_session()

    def define_fields(self, entity: str) -> List:
        entity = globals()[entity]()
        return entity.get_fields()

    def loadMainTable(self):
        self.entity = globals()[self.ui.comboBox.currentText()]

        headers = self.define_fields(self.ui.comboBox.currentText())
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        data = show_all(self.entity)
        model.setRowCount(len(data))

        for row, obj in enumerate(data):
            # if obj["orders"] == None:
            #     o = "-"
            # else:
            #     o = str([id for id in employee["orders"]])
            for index, field in enumerate(headers):
                model.setItem(row, index, QtGui.QStandardItem(str(obj[field])))

            # model.setItem(row, 1, QtGui.QStandardItem(obj[field]))
            # model.setItem(row, 2, QtGui.QStandardItem(obj["username"]))
            # model.setItem(row, 3, QtGui.QStandardItem(obj["password"]))
            # model.setItem(row, 4, QtGui.QStandardItem(o))


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
            obj_id = int(id_.data(0))
            obj = query_find_by_id(self.entity, obj_id)
            for index, field in enumerate(obj.get_fields()):
                if item.column() == index + 1:
                    obj.property[field] = item.data(0)
        else:
            # self.temp_obj = create_obj(globals()[self.ui.comboBox.currentText()]())

            for index, field in enumerate(self.define_fields(self.ui.comboBox.currentText())):
                if item.column() == index:
                    model.setData(model.index(item.row(), item.column()), item.data(0))
                    # self.temp_obj.property[field] = item.data(0)
                    self.temp_obj[field] = item.data(0)

            # model.submit()

            # print("Данные из ячейки в модели:")
            # print(model.index(item.row(), item.column()).data(0))
            #
            # print("Данные из всех ячеек в модели:")
            # print(model.index(item.row(), 1).data(0))
            # print(model.index(item.row(), 2).data(0))
            # print(model.index(item.row(), 3).data(0))
            #
            # print("Данные из полей временного объекта:")
            # print(self.temp_obj["name"])
            # print(type(self.temp_obj["name"]))
            # print(self.temp_obj["username"][1])
            # print(self.temp_obj["password"][1])


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
        self.temp_obj = create_obj(self.ui.comboBox.currentText())

    def saveDataInNewRow(self, i):
        new_obj = add_obj(self.ui.comboBox.currentText())
        model = self.ui.mainTableView.model()

        # print("Данные из полей временного employee в сейвметоде:")
        # print(self.temp_employee["name"][1])
        # print(self.temp_employee["username"][1])
        # print(self.temp_employee["password"][1])

        for str_key, value in self.temp_obj.items():
            # field = str_field.strip()
            # field = trim(str_field, , '"')
            setattr(new_obj, str_key, value)
            # new_obj.field = self.temp_obj[str_field]

        for index, str_field in enumerate(self.temp_obj.keys()):
            self.temp_obj[str_field] = ""

        commit_session()
        print("Adding method is working")
        self.ui.lcdNumber.display(model.rowCount())
        self.loadMainTable()

    def onDeleteRowPBClicked(self):
        model = self.ui.mainTableView.model()
        if self.ui.mainTableView.currentIndex().row() > -1:
            row_index = self.ui.mainTableView.currentIndex().row()
            txt = model.takeItem(self.ui.mainTableView.currentIndex().row(), 0).text()
            id = int(txt)
            model.removeRow(row_index)
            delete_obj(self.entity, id)
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


