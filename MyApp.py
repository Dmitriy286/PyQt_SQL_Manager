from typing import List, Optional, Union
import time

from PySide2 import QtWidgets, QtCore, QtGui

from ui.Form import Ui_MainWindow
from Model import init_db, commit_session, Employee, Customer, Order
from Controller import delete_obj, \
    create_obj, add_obj, show_all, query_find_by_id, save_in_base, query_find_employee_by_name


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
        self.loadMainTable(None)

        self.initThreads()
        self.initSignals()

        # self.initThreads()
        # self.temp_obj = create_obj()
        self.temp_obj = {}
        o = Employee()
        setattr(o, 'id', 100)
        print(o.__dict__)
        print(o.__dict__['id'])

    def initSignals(self):
        self.ui.addRowPB.clicked.connect(self.onAddRowPBClicked)
        self.ui.deleteRowPB.clicked.connect(self.onDeleteRowPBClicked)
        self.ui.savePB.clicked.connect(self.onSavePBClicked)
        self.ui.showAllPB.clicked.connect(self.onShowAllPBClicked)
        self.ui.findPB.clicked.connect(self.onFindPBClicked)

        # self.ui.comboBox.currentTextChanged.connect(self.first_thread_start_stop)
        self.ui.comboBox.currentTextChanged.connect(self.loadMainTable)

        # self.threadOne.mysignal.connect(self.setPlainTextEditConsole, QtCore.Qt.AutoConnection)
        self.threadTwo.mysignal.connect(self.setPlainTextEditConsole, QtCore.Qt.AutoConnection)
        self.threadTwo.mysignal.connect(self.load_secondary_table, QtCore.Qt.AutoConnection)

        # self.threadOne.started.connect(self.start..)
        # self.threadOne.finished.connect(self.stop...)

        self.ui.mainTableView.clicked.connect(self.second_thread_start_stop)
        #
        # self.ui.deleteRowPB.installEventFilter(self)
        # self.ui.addRowPB.installEventFilter(self)

        self.ui.mainTableView.installEventFilter(self)

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
        self.loadMainTable(None)

    def define_fields(self, entity: str) -> List:
        entity = globals()[entity]()
        return entity.get_fields()

    def loadMainTable(self, data_list: Union[List, int, None]):
        self.entity = globals()[self.ui.comboBox.currentText()]

        headers = self.define_fields(self.ui.comboBox.currentText())
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        print(f"Данные, поступающие в метод загрузки таблицы: {data_list}")
        if data_list is None or isinstance(data_list, str):
            data = show_all(self.entity)
        else:
            data = data_list
        model.setRowCount(len(data))
        print(f"Данные, поступающие в таблицу: {data}")
        for row, obj in enumerate(data):
            for index, field in enumerate(headers):
                model.setItem(row, index, QtGui.QStandardItem(str(obj[field])))


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

            if self.ui.checkBox.isChecked():
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
        self.loadMainTable(None)

    def onDeleteRowPBClicked(self):
        model = self.ui.mainTableView.model()
        if self.ui.mainTableView.currentIndex().row() > -1:
            row_index = self.ui.mainTableView.currentIndex().row()
            model.removeRow(row_index)
            txt = model.takeItem(self.ui.mainTableView.currentIndex().row(), 0).text() #todo проверка на непустую строку
            id = int(txt)
            delete_obj(self.entity, id)
            self.ui.lcdNumber.display(model.rowCount())
        else:
            QtWidgets.QMessageBox.question(self, 'Message', "Please select a row to delete", QtWidgets.QMessageBox.Ok)

        commit_session()

        print("Delete method works")
        self.ui.lcdNumber.display(model.rowCount())

    def onFindPBClicked(self):
        self.setPlainTextEditConsole(f"Текущая сущность: {self.ui.plainTextEdit.toPlainText()}")
        time.sleep(2)
        data = query_find_employee_by_name(self.ui.plainTextEdit.toPlainText())
        self.setPlainTextEditConsole(f"Список найденных по имени ({data})")
        time.sleep(2)
        self.loadMainTable(data)

    def event(self, event: QtCore.QEvent) -> bool:
        pass

        return QtWidgets.QWidget.event(self, event)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if watched == self.ui.mainTableView and event.type() == QtCore.QEvent.KeyPress:
            print(f"key {event.text()} pressed")
            print(event.type())
            if event.key() == QtCore.Qt.Key_Delete:
                self.onDeleteRowPBClicked()
                print(event.text())

        if watched == self.ui.mainTableView and event.type() == QtCore.QEvent.KeyPress:
            print(f"key {event.text()} pressed")
            print(event.type())
            if event.key() == QtCore.Qt.Key_Plus:
                self.onAddRowPBClicked()
                print(event.text())

        return super(MyApp, self).eventFilter(watched, event)

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
        # self.params = None #todo сеттер
        #
        # self.db_model_obj = None

    def run(self):

        # self.db_model_obj.filter...

        self.status = True
        count = 5
        while self.status:
            time.sleep(2)
            # fetch all -> emit
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




