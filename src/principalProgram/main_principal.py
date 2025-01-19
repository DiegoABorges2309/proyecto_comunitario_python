import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QLineEdit, QFrame
from PyQt5.uic import loadUi
import img.img_qrc
from src.db.__init__ import init, close
import asyncio
from src.db.crud import UserLogin, ItemInventory

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login_interface.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # botton x
        self.x.clicked.connect(self.close)
        # botton -
        self.o.clicked.connect(self.showMinimized)
        # login
        self.IngresarBoton.clicked.connect(self.action)
        # inputs
        self.contrasenaEdit.setEchoMode(QLineEdit.Password)
        # otra
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
                self.run(_dates, _user)
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
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")
        await close()

    def run(self, date, _user):
        self.program = MainPrincipal(date, _user)
        self.program.show()

class MainPrincipal(QDialog):
    def __init__(self, _date, _user):
        super(MainPrincipal, self).__init__()
        loadUi('principalProgram.ui', self)
        # Texto de usuario:
        self.profile.setText(_user)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # botton x
        self.pushButton_3.clicked.connect(self.close)
        # botton -
        self.pushButton_6.clicked.connect(self.showMinimized)
        #boton agg:
        self.addInsumo.clicked.connect(lambda : self.show_agg_frame())
        # frame agg:
        self.aggFrame.hide()
        # tabla
        self.inventario.verticalHeader().hide()
        self.inventario.setShowGrid(True)
        self.inventario.setGridStyle(QtCore.Qt.SolidLine)
        style = "QTableWidget { gridline-color: #e7eff7; background: none; color: rgb(70, 79, 78); padding: 2px;}"
        self.inventario.setStyleSheet(style)
        # botonbuscar
        self.pushButton_4.clicked.connect(self.actions)
        # Menu:
        self.show_items(_date)
        self.editarFrame.hide()
        self.editarFrame_2.hide()
        self.actualizarFrame.hide()
        self.eliminarFrame.hide()
        self.exelFrame.hide()

    def show_items(self, _dates):
        index_b = 0
        for row in _dates:
            index_b += 1
        index_a = 0
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

            self.inventario.setItem(index_a, 0, item_one)
            self.inventario.setItem(index_a, 1, item_two)
            self.inventario.setItem(index_a, 2, item_tre)
            self.inventario.setItem(index_a, 3, item_four)
            self.inventario.setItem(index_a, 4, item_five)
            self.editarBoton = QtWidgets.QPushButton()
            self.editarBoton.setText("Editar")
            self.editarBoton.clicked.connect(lambda _, date = row, _pos = self.editarBoton.geometry().x() : self.edit(date, _pos))
            self.editarBoton.setStyleSheet("""QPushButton{
        	                                  background: transparent;
        	                                  border: none;
        	                                  background-color: rgb(84, 194, 143);
        	                                  color: rgb(18, 31, 48);
        	                                  background-color: rgb(106, 215, 225);
        	                                  border-radius: 5px;
        	                                  margin-left: 52px;
        	                                  margin-right: 52px;
        	                                  margin-top: 3px;
        	                                  margin-bottom: 3px;
                                          }

                                          QPushButton:pressed{
        	                                  background-color: rgb(255, 255, 255);
                                          }""")

            self.inventario.setCellWidget(index_a, 5, self.editarBoton)
            index_a += 1

        self.inventario.horizontalHeader().setStretchLastSection(True)

    def edit(self, date, _pos):
        try:
            asyncio.run(self._upgrade(date.name_item))
            buttom = self.sender()
            position = buttom.pos()

            if buttom and position.y() < 300:
                self.editarFrame.setGeometry(position.x()-45, position.y()+47, 111, 141)
                self.editarFrame.show()
            else:
                self.editarFrame.setGeometry(position.x() - 45, 345, 111, 141)
                self.editarFrame.show()

            self.editarFrame_2.hide()
            self.actualizarFrame.hide()
            self.eliminarFrame.hide()
            self.exelFrame.hide()
            self.aggFrame.hide()

            self.actualizar.clicked.connect(lambda: self._show_buttom(position.x()-45, position.y()+47, date,
                                        397, self.actualizarFrame, 301, 111))
            self.editar.clicked.connect(lambda: self._show_buttom(position.x()-175, position.y()+47, date,
                                        250, self.editarFrame_2, 441, 271))
            self.eliminar.clicked.connect(lambda: self._show_buttom(position.x()-45, position.y()+47, date,
                                        397, self.eliminarFrame, 301, 111))
        except Exception as e:
            print(e)

    async def _upgrade(self, _name):
        ii = ItemInventory()
        await init()
        await ii.update_item(_name)
        await close()

    def actions(self):
        try:
            text = self.lineEdit.text()
            asyncio.run(self.search(text))
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")
            print(f"ERROR:{e}")

    async def search(self, _name_item):
        ii = ItemInventory()
        await init()
        result = await ii.get_ones_item(_name_item)
        if result[0] != None:
            self.show_items(result)
        await close()

    def _show_buttom(self, pos_x, pos_y, date, limite, frame_show, tamx, tamy):
        try:
            self.label_5.setText(date.name_item)
            self.label_7.setText(date.name_item)
            self.label_9.setText(date.name_item)
            if pos_y > limite:
                frame_show.setGeometry(pos_x - 200, limite, tamx, tamy)
            else:
                frame_show.setGeometry(pos_x - 200, pos_y, tamx, tamy)
            self.editarFrame.hide()
            frame_show.show()
            print(date.name_item)
            # agregados:
            self.actualizarLine_3.setText(date.name_item)
            self.actualizarLine_4.setText(date.unit)
            self.actualizarLine_5.setText(str(date.quantity))
            self.actualizarLine_6.setText(date.lot)
            self.actualizarLine_7.setText(str(date.exp))
        except Exception as e:
            print(e)

    def show_agg_frame(self):
        self.actualizarLine_11.setText('')
        self.actualizarLine_12.setText('')
        self.actualizarLine_13.setText('')
        self.actualizarLine_14.setText('')
        self.actualizarLine_15.setText('')
        self.editarFrame.hide()
        self.editarFrame_2.hide()
        self.actualizarFrame.hide()
        self.eliminarFrame.hide()
        self.exelFrame.hide()
        self.aggFrame.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = Login()
    program.show()
    sys.exit(app.exec_())
