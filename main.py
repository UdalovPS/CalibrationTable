import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from calibration_py import Ui_CalibrationWindow
from add_py import Ui_InsertWindow
import sys
import language
import database
import os
import read_excel

LNG = 'rus'

class Calibration(QtWidgets.QMainWindow):
    def __init__(self):
        super(Calibration, self).__init__()
        self.ui = Ui_CalibrationWindow()
        self.ui.setupUi(self)
        self.widget_text()
        # self.tanks = language.CalibrationLng(LNG).tanks
        # self.products = language.CalibrationLng(LNG).products
        self.ui.pushButton.clicked.connect(lambda: self.select_value())
        self.ui.redactBtn.clicked.connect(lambda: self.open_redact_window())

    def widget_text(self):
        t = language.CalibrationLng(LNG)
        self.setWindowTitle(t.title)
        self.ui.tankLabel.setText(t.tankLbl)
        self.ui.levelLabel.setText(t.levelLbl)
        self.ui.productLabel.setText(t.productLbl)
        self.ui.tempLabel.setText(t.tempLbl)
        self.ui.pushButton.setText(t.textBtn)
        self.ui.volumeLabel.setText(t.volume)
        self.ui.densityLabel.setText(t.density)
        self.ui.massLabel.setText(t.mass)
        self.ui.tankBox.addItems(self.select_from_db(tanks=1))
        self.ui.productEdit.addItems(self.select_from_db(prod=1))
        self.ui.choiceBox.addItems(t.choiceBox)
        self.ui.redactBtn.setText(t.redactBtn)

    def open_redact_window(self):
        w = AddWindow()
        w.show()
        self.close()

    def select_from_db(self, prod=None, tanks=None):
        if prod:
            field = 'prodName'
            table_name = 'product'
        if tanks:
            field = 'name'
            table_name = 'names'
        tmp_list = []
        sel = database.AddDataTable()
        data = sel.select_from_db(table_name, field=field)
        for item in data:
            tmp_list.append(item[0])
        return tmp_list

    def clear_widget(self, straight=None, back=None):
        if straight:
            self.ui.volumeEdti.clear()
            self.ui.densityEdit.clear()
            self.ui.massEdit.clear()
        if back:
            self.ui.levelEdit.clear()
            self.ui.tempEdit.clear()

    def select_value(self):
        if self.ui.choiceBox.currentText() == '>>>':
            self.straight_calc()
        else:
            self.back_calc()

    def straight_calc(self):
        self.clear_widget(straight=1)
        field = 'volume'
        cond = "name = '{0}'"   .format(self.ui.tankBox.currentText())
        table_name = database.DataBase().select_from_db('names',
                                                        cond, 'codName')
        table_name = table_name[0][0]
        level = self.ui.levelEdit.text()
        cond = 'level = {0}'.format(level)
        try:
            volume = database.DataBase().select_from_db(table_name,
                                                        cond, field)
            self.ui.volumeEdti.setText(str(volume[0][0]))
        except(IndexError, sqlite3.OperationalError):
            text = language.CalibrationLng(LNG).levelError
            self.show_error(text[0], text[1])
        temp = self.ui.tempEdit.text()
        if temp: self.find_mass(temp, volume[0][0])

    def back_calc(self):
        self.clear_widget(back=1)
        field = 'min(level)'
        cond = "name = '{0}'"   .format(self.ui.tankBox.currentText())
        table_name = database.DataBase().select_from_db('names',
                                                        cond, 'codName')
        table_name = table_name[0][0]
        if self.ui.massEdit.text():
            volume = self.calc_volume()
        else:
            try:
                volume = float(self.ui.volumeEdti.text())
            except(IndexError, ValueError):
                text = language.CalibrationLng(LNG).volumeError
                self.show_error(text[0], text[1])
        cond = 'volume >= {0}'.format(volume)
        try:
            level = database.DataBase().select_from_db(table_name,
                                                       cond, field)
            self.ui.levelEdit.setText(str(level[0][0]))
        except(IndexError, sqlite3.OperationalError):
            text = language.CalibrationLng(LNG).backError
            self.show_error(text[0], text[1])

    def calc_volume(self):
        try:
            mass = float(self.ui.massEdit.text())
        except(IndexError, ValueError):
            text = language.CalibrationLng(LNG).massError
            self.show_error(text[0], text[1])
        try:
            density = float(self.ui.densityEdit.text())
        except(IndexError, ValueError):
            text = language.CalibrationLng(LNG).massError
            self.show_error(text[0], text[1])
        volume = mass / density
        volume = round(volume, 3)
        self.ui.volumeEdti.setText(str(volume))
        return volume


    def find_mass(self, temp=None, volume=None):
        r = ((0.6500, 0.6599, 0.000962), (0.6600, 0.6699, 0.000949),
             (0.6700, 0.6799, 0.000936), (0.6800, 0.6899, 0.000925),
             (0.6900, 0.6999, 0.00091), (0.7000, 0.7099, 0.000897),
             (0.7100, 0.7199, 0.000884), (0.7200, 0.7299, 0.00087),
             (0.7300, 0.7399, 0.000857), (0.7400, 0.7499, 0.000844),
             (0.7500, 0.7599, 0.000831), (0.7600, 0.7699, 0.000818),
             (0.7700, 0.7799, 0.000805), (0.7800, 0.7899, 0.000792),
             (0.7900, 0.7999, 0.000778), (0.8000, 0.8099, 0.000765),
             (0.8100, 0.8199, 0.000752), (0.8200, 0.8299, 0.000738),
             (0.8300, 0.8399, 0.000725), (0.8400, 0.8499, 0.000712),
             (0.8500, 0.8599, 0.000699), (0.8600, 0.8699, 0.000686),
             (0.8700, 0.8799, 0.000673), (0.8800, 0.8899, 0.00066),
             (0.8900, 0.8999, 0.000647), (0.9000, 0.9099, 0.000633),
             (0.9100, 0.9199, 0.00062), (0.9200, 0.9299, 0.000607),
             (0.9300, 0.9399, 0.000594), (0.9400, 0.9499, 0.000581),
             (0.9500, 0.9599, 0.000567), (0.9600, 0.9699, 0.000554),
             (0.9700, 0.9799, 0.000541), (0.9800, 0.9899, 0.000528),
             (0.9900, 1.0000, 0.000515)
             )
        cond = "prodName = '{0}'".format(self.ui.productEdit.currentText())
        p20 = database.DataBase().select_from_db('product', cond,
                                                 'density')
        p20 = p20[0][0]
        for i in r:
            if i[0] <= p20 <= i[1]:
                break
        alfa = i[2]
        try:
            density = float(p20) - alfa * (float(temp)-20)
            self.ui.densityEdit.setText(str(round(density, 3)))
            mass = volume * density
            self.ui.massEdit.setText(str(round(mass, 3)))
        except(ValueError):
            text = language.CalibrationLng(LNG).tempError
            self.show_error(text[0], text[1])

    def show_error(self, title, message):
        error = QMessageBox()
        error.setWindowTitle(title)
        error.setText(message)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()


class Function():
    def make_table(self):
        make = database.AddDataTable()

    def insert_table_in_sql(self, table_name, data):
        data_fields = ('level, volume')
        self.make_sql_tbl(table_name)
        ins = database.DataBase()
        ins.insert_many(table_name, data)

    def make_sql_tbl(self, table_name):
        db_name = 'db.db'
        table_fields = 'level INTEGER, volume REAL'
        make = database.DataBase()
        make.make_table(table_name, table_fields)

class AddWindow(QtWidgets.QMainWindow, Function):
    def __init__(self):
        super(AddWindow, self).__init__()
        self.ui = Ui_InsertWindow()
        self.ui.setupUi(self)
        self.widget_text()
        self.update_boxs()
        self.ui.addProductBtn.clicked.connect(lambda: self.add_product())
        self.ui.delProductBtn.clicked.connect(lambda: self.del_product())
        self.ui.addTableBtn.clicked.connect(lambda: self.add_table())
        self.ui.delTableBtn.clicked.connect(lambda: self.del_table())
        self.ui.backBtn.clicked.connect(lambda: self.back_func())

    def back_func(self):
        w = Calibration()
        w.show()
        self.close()

    def widget_text(self):
        t = language.AddWindow(LNG)
        self.setWindowTitle(t.title)
        self.ui.addLabel.setText(t.addLabel)
        self.ui.codNameLabel.setText(t.codNameLabel)
        self.ui.nameTableLabel.setText(t.nameTableLabel)
        self.ui.typeLabel.setText(t.typeLabel)
        self.ui.fileLabel.setText(t.fileLabel)
        self.ui.addProduct.setText(t.addProduct)
        self.ui.productNameLabel.setText(t.productNameLabel)
        self.ui.valueLabel.setText(t.valueLabel)
        self.ui.delTableLabel.setText(t.delTableLabel)
        self.ui.delProductLabel.setText(t.delProductLabel)
        self.ui.addTableBtn.setText(t.add)
        self.ui.addProductBtn.setText(t.add)
        self.ui.delTableBtn.setText(t.delete)
        self.ui.delProductBtn.setText(t.delete)
        self.ui.typeBox.addItems(t.typeBox)
        self.ui.fileBox.addItems(self.excel_files_list())
        self.ui.backBtn.setText(t.back)

    def excel_files_list(self):
        file_list = []
        for file_name in os.listdir():
            if file_name[-4:] == 'xlsx':
                file_list.append(file_name)
        return file_list

    def del_table(self):
        text_message = language.AddWindow(LNG)
        dell = database.AddDataTable()
        name = self.ui.delTableBox.currentText()
        cond = "name = '{0}'".format(name)
        cod_name = dell.select_from_db(dell.table_with_names,
                                       cond, 'codName')
        cod_name = cod_name[0][0]
        dell.delete_from_db(dell.table_with_names, cond)
        delete = database.DataBase()._delete_table(cod_name)
        self.update_boxs()
        self.show_ok(text_message.del_table_msg[0],
                     text_message.del_table_msg[1])

    def del_product(self):
        text_msg = language.AddWindow(LNG).del_prod_msg
        dell = database.AddDataTable()
        product_density = self.ui.delProductBox.currentText()
        name = product_density.partition('=')[0][0:-1]
        cond = "prodName = '{0}'".format(name)
        dell.delete_from_db(dell.table_with_density, cond)
        self.update_boxs()
        self.show_ok(text_msg[0], text_msg[1])

    def add_product(self):
        text_msg = language.AddWindow(LNG)
        try:
            prod_name = self.ui.productNameEdit.text()
            value = float(self.ui.valueEdit.text())
            add = database.AddDataTable()
            add.insert_in_table(add.table_with_density,
                                add.prod_data_fields,
                                (prod_name, value))
            self.update_boxs()
            self.show_ok(text_msg.add_prod_msg[0],
                         text_msg.add_prod_msg[1])
        except(ValueError):
            self.show_error(text_msg.data_error[0],
                            text_msg.data_error[1])

    def add_table(self):
        try:
            text = language.AddWindow(LNG).data_add_msg
            self.show_ok(text[0], text[1])
            add = database.AddDataTable()
            type_tank =  self.ui.typeBox.currentText()
            cod_name = self.ui.codNameEdit.text()
            name = self.ui.nameLabelEdit.text()
            file_name = self.ui.fileBox.currentText()
            if type_tank == 'РВС':
                data_for_file = read_excel.OpenXl(file_name).open_rvs()
            if type_tank == 'РГС':
                data_for_file = read_excel.OpenXl(file_name).open_rgs()
            # print(data_for_file)
            self.insert_table_in_sql(cod_name, data_for_file)
            add.insert_in_table(add.table_with_names,
                        add.names_data_fields,
                        (cod_name, name))
            self.update_boxs()
            text_message = language.AddWindow(LNG).save_db
            self.show_ok(text_message[0], text_message[1])
        except(IndexError, ValueError):
            text = language.AddWindow(LNG).data_for_sql
            self.show_error(text[0], text[1])

    def update_boxs(self):
        t = language.AddWindow(LNG)
        prod_names = []
        tanks_names = []
        sel = database.AddDataTable()
        product = sel.select_from_db(sel.table_with_density,
                                  field='prodName, density')
        tanks = sel.select_from_db(sel.table_with_names,
                                   field='name')
        for prod in product:
            prod_names.append(prod[0] + ' = ' + str(prod[1]) + t.density)
        for name in tanks:
            tanks_names.append(name[0])
        self.ui.delProductBox.clear()
        self.ui.delTableBox.clear()
        self.ui.delProductBox.addItems(prod_names)
        self.ui.delTableBox.addItems(tanks_names)

    def show_error(self, title, message):
        error = QMessageBox()
        error.setWindowTitle(title)
        error.setText(message)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    def show_ok(self, title='ok', message='ok'):
        error = QMessageBox()
        error.setWindowTitle(title)
        error.setText(message)
        error.setIcon(QMessageBox.Information)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Calibration()
    # w = AddWindow()
    w.show()
    sys.exit(app.exec())

