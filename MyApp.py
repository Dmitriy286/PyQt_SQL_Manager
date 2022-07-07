from typing import List
import time

from PySide2 import QtWidgets, QtCore, QtSql, QtGui, QtSql
from PySide2.QtGui import QStandardItem, Qt
from PySide2.QtSql import QSqlTableModel
from sqlalchemy import column
from sqlalchemy.engine import row

from Form import Ui_MainWindow
from Model import init_db, Employee, Customer, Order, del_db, commit_session, get_type
from Controller import delete_obj, \
    create_obj, add_obj, show_all, query_find_by_id, save_in_base
# from SecondThread import SecondaryTable


class MyApp(QtWidgets.QMainWindow):
    current_secondary_table_name = None

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        # del_db()
        init_db()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entity = None
        self.secondary_table_entity = None
        self.loadMainTable()

        self.initThreads()
        self.initSignals()

        # self.initThreads()
        # self.temp_obj = create_obj()
        self.temp_obj = {}




    def initSignals(self):
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        self.ui.savePB.clicked.connect(self.onSavePBClicked)
        self.ui.showAllPB.clicked.connect(self.onShowAllPBClicked)

        # self.ui.comboBox.currentTextChanged.connect(self.first_thread_start_stop)
        self.ui.comboBox.currentTextChanged.connect(self.loadMainTable)

        # self.threadOne.mysignal.connect(self.setPlainTextEditConsole, QtCore.Qt.AutoConnection)
        self.threadTwo.mysignal.connect(self.setPlainTextEditConsole, QtCore.Qt.AutoConnection)
        self.threadTwo.mysignal.connect(self.load_secondary_table, QtCore.Qt.AutoConnection)

        # self.threadOne.started.connect(self.start..)
        # self.threadOne.finished.connect(self.stop...)

        self.ui.mainTableView.clicked.connect(self.second_thread_start_stop)

    def initThreads(self):
        # self.threadOne = MainTable()
        self.threadTwo = SecondaryTable()

        # self.threadOne.start()

    def setPlainTextEditConsole(self, text):
        self.ui.plainTextEditConsole.clear()
        self.ui.plainTextEditConsole.appendPlainText(text)

    # def first_thread_start_stop(self):
    #     self.threadOne.stop()
    #     self.setLineEditText("First thread is stopped")
    #     time.sleep(2)
    #     self.setLineEditText("Starting first thread")
    #     self.threadOne.start()

    def second_thread_start_stop(self, item: QtCore.QModelIndex):
        if "employee_id" in self.define_fields(self.ui.comboBox.currentText()) \
        and "customer_id" in self.define_fields(self.ui.comboBox.currentText()):
            print(self.define_fields(self.ui.comboBox.currentText()))
            print(self.define_fields(self.ui.comboBox.currentText()).index("employee_id"))
            print(item.column())
            if item.column() == self.define_fields(self.ui.comboBox.currentText()).index("employee_id"):
                self.threadTwo.entity = globals()["Employee"]
                self.stopSecondThread()
                self.setPlainTextEditConsole("Second thread is stopped")
                # time.sleep(2)
                self.setPlainTextEditConsole("Starting second thread")
                self.start_thread_two("Employee")

            elif item.column() == self.define_fields(self.ui.comboBox.currentText()).index("customer_id"):
                self.threadTwo.entity = globals()["Customer"]
                self.stopSecondThread()
                self.setPlainTextEditConsole("Second thread is stopped")
                # time.sleep(2)
                self.setPlainTextEditConsole("Starting second thread")
                self.start_thread_two("Customer")

            else:
                self.setPlainTextEditConsole("Связанная сущность к текущей колонке отсутствует")

        else:
            self.setPlainTextEditConsole("В текущей таблице нет внешних ключей")

    def start_thread_two(self, e):
        self.secondary_table_entity = globals()[e]
        self.threadTwo.start()

    def stopSecondThread(self):
        self.threadTwo.status = False

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
            for index, field in enumerate(headers):
                model.setItem(row, index, QtGui.QStandardItem(str(obj[field])))

            # model.setItem(row, 1, QtGui.QStandardItem(obj[field]))
            # model.setItem(row, 2, QtGui.QStandardItem(obj["username"]))
            # model.setItem(row, 3, QtGui.QStandardItem(obj["password"]))
            # model.setItem(row, 4, QtGui.QStandardItem(o))

        self.ui.mainTableView.setModel(model)

        self.ui.mainTableView.horizontalHeader().setSectionsMovable(True)
        self.ui.mainTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.setPlainTextEditConsole(f"{self.ui.comboBox.currentText()} table loaded")
        self.ui.lcdNumber.display(model.rowCount())

        model.dataChanged.connect(self.mainTableViewDataChanged)

    def load_secondary_table(self):
        model = QtGui.QStandardItemModel()
        self.ui.secondaryTableView.setModel(model)

        headers = ['id', 'name']

        model.setHorizontalHeaderLabels(headers)

        data = show_all(self.secondary_table_entity)
        model.setRowCount(len(data))

        for row, obj in enumerate(data):
            model.setItem(row, 0, QtGui.QStandardItem(str(obj["id"])))
            model.setItem(row, 1, QtGui.QStandardItem(obj["name"]))

        self.ui.secondaryTableView.horizontalHeader().setSectionsMovable(True)
        self.ui.secondaryTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def mainTableViewDataChanged(self, item: QtCore.QModelIndex):
        model = self.ui.mainTableView.model()
        print(item.data(0))

        id_= model.index(item.row(), 0)

        if id_.data(0) != None:
            obj_id = int(id_.data(0))
            temp_obj = create_obj(self.ui.comboBox.currentText())
            obj = query_find_by_id(self.entity, obj_id)
            for index, field in enumerate(obj.get_fields()):
                if item.column() == index:
                    if isinstance(temp_obj[field], int):
                        setattr(obj, field, int(item.data(0)))
                    else:
                        setattr(obj, field, item.data(0))

            if self.ui.checkBox.setChecked():
                commit_session()

        else:
            for index, field in enumerate(self.define_fields(self.ui.comboBox.currentText())):
                if item.column() == index:
                    model.setData(model.index(item.row(), item.column()), item.data(0))
                    # self.temp_obj.property[field] = item.data(0)
                    if isinstance(self.temp_obj[field], int):
                        self.temp_obj[field] = int(item.data(0))
                    else:
                        self.temp_obj[field] = item.data(0)

            # model.submit()

    def onSavePBClicked(self):
        model = self.ui.mainTableView.model()
        index = model.rowCount() - 1
        if model.item(index, 0) != None:
            print("Save button is working. Change is saving")
            commit_session()
        else:
            print("Save button is working. New row is saving")
            self.saveDataInNewRow()

    def onAddRowPBClicked(self):
        model = self.ui.mainTableView.model()
        index = model.rowCount()
        model.insertRows(index, 1)
        self.temp_obj = create_obj(self.ui.comboBox.currentText())

    def saveDataInNewRow(self):
        print(self.temp_obj)
        new_obj = add_obj(self.ui.comboBox.currentText())
        print(new_obj)
        model = self.ui.mainTableView.model()

        for str_key, value in self.temp_obj.items():
            if isinstance(value, int):
                setattr(new_obj, str_key, int(value))
            else:
                setattr(new_obj, str_key, value)

        save_in_base(new_obj)
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

# class MainTable(QtCore.QThread):
#     mysignal = QtCore.Signal(str)
#
#     def __init__(self, parent=None):
#         super(MainTable, self).__init__(parent)
#         self.entity = None
#
#     def run(self):
#         MyApp.loadMainTable()
#
#         self.mysignal.emit("First thread started. Main table is loading...")

class SecondaryTable(QtCore.QThread):
    mysignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(SecondaryTable, self).__init__(parent)

    def run(self):
        self.status = True
        count = 5
        while self.status:
            time.sleep(2)
            self.mysignal.emit(f"Загрузка второй таблицы: {count}")
            count -= 1
            if count == -1:
                self.mysignal.emit("Вторая таблица загружена")
                break

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()


