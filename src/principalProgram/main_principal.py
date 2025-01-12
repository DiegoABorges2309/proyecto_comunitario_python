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
        #datos:
        self.date = _date
        self.lines = _lines
        self.inventario.setRowCount(self.lines)
        index_a = 0
        for row in self.date:
            print(self.date[0])
            for cell in row:
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            index_a += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = Login()
    program.show()
    sys.exit(app.exec_())


