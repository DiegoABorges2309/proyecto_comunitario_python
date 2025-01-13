import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidget
from PyQt5.uic import loadUi
import img_qrc
from src.db.__init__ import init, close
import asyncio
from src.db.crud import UserLogin, ItemInventory
from qasync import QEventLoop

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login_interface.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # botton x
        self.x.clicked.connect(self.close)
        # botton -
        self.o.clicked.connect(self.showMinimized)
        #login
        self.IngresarBoton.clicked.connect(self.action)
        #otra
        self.program = None


    def action(self):
        asyncio.run(self.get_text())

    async def get_text(self):
        try:
            await init()
            _user = self.usuarioEdit.text()
            _password = self.contrasenaEdit.text()
            lg = UserLogin()
            result = await lg.verific_user(_user, _password)
            if result:
                _dates = await self.get_date()
                self.close()
                self.run(_dates)
            else:
                QtWidgets.QMessageBox.information(self, "Sistema de Almacen", "Acceso Denegado")
            await close()
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")

    async def get_date(self):
        await init()
        try:
            crud = ItemInventory()
            dates = await crud.get_all_item()
            return dates
        except Exception as e:
            QtWidgets.QMessageBox.information(self,"Sistema de Almacen", f"{e}")
        await close()

    def run(self, date):
        lines = 0
        for row in date:
            lines += 1
        self.program = MainPrincipal(date, lines)
        self.program.show()

class MainPrincipal(QDialog):
    def __init__(self, _date, _lines):
        super(MainPrincipal, self).__init__()
        loadUi('principalProgram.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #botton x
        self.pushButton_3.clicked.connect(self.close)
        #botton -
        self.pushButton_6.clicked.connect(self.showMinimized)
        #tabla
        self.inventario.verticalHeader().hide()
        self.inventario.setShowGrid(True)
        self.inventario.setGridStyle(QtCore.Qt.SolidLine)
        style = "QTableWidget { gridline-color: #e7eff7; background: none; color: rgb(70, 79, 78); padding: 2px;}"
        self.inventario.setStyleSheet(style)
        #datos:
        self.date = _date
        self.lines = _lines
        self.inventario.setRowCount(self.lines)
        #botonbuscar
        self.pushButton_4.clicked.connect(self.actions)
        index_a = 0
        for row in self.date:
            item_one = QtWidgets.QTableWidgetItem(str(row.name_item))
            item_two = QtWidgets.QTableWidgetItem(str(row.quantity))
            item_tre = QtWidgets.QTableWidgetItem(str(row.unit))
            item_four = QtWidgets.QTableWidgetItem(str(row.lot))
            item_five = QtWidgets.QTableWidgetItem(str(row.exp))

            # item_one.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_one.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
#             item_two.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_two.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
#             item_tre.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_tre.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
#             item_four.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_four.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
#             item_five.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_five.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.inventario.setItem(index_a, 0, item_one)
            self.inventario.setItem(index_a, 1, item_two)
            self.inventario.setItem(index_a, 2, item_tre)
            self.inventario.setItem(index_a, 3, item_four)
            self.inventario.setItem(index_a, 4, item_five)
            index_a += 1

    def actions(self):
        try:
            text = self.lineEdit.text()
            asyncio.run(self.search(text))
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")

    async def search(self, _name_item):
        ii = ItemInventory()
        await init()
        result = await ii.get_ones_item(_name_item)
        if result[0] != None:
            await self.upgrade(result)
        await close()

    async def upgrade(self, _dates):
        index_b = 0
        index_c = 0
        for row in _dates:
            index_b += 1
        self.inventario.setRowCount(index_b)
        for row in _dates:
            item_one = QtWidgets.QTableWidgetItem(str(row.name_item))
            item_two = QtWidgets.QTableWidgetItem(str(row.quantity))
            item_tre = QtWidgets.QTableWidgetItem(str(row.unit))
            item_four = QtWidgets.QTableWidgetItem(str(row.lot))
            item_five = QtWidgets.QTableWidgetItem(str(row.exp))

            # item_one.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_one.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #             item_two.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_two.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #             item_tre.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_tre.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #             item_four.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_four.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #             item_five.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
            item_five.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.inventario.setItem(index_c, 0, item_one)
            self.inventario.setItem(index_c, 1, item_two)
            self.inventario.setItem(index_c, 2, item_tre)
            self.inventario.setItem(index_c, 3, item_four)
            self.inventario.setItem(index_c, 4, item_five)
            index_c += 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = Login()
    program.show()
    sys.exit(app.exec_())


