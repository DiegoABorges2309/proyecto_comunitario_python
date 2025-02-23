import asyncio
import sys
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.uic import loadUi
from src.db.__init__ import init, close
from src.db.crud import UserLogin, ItemInventory, ExelInventory
from functions import Functions
from img import img_qrc


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
        #loop asyncio:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.func = Functions()
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
        self.indicator = False
        self.inventario.verticalHeader().hide()
        self.inventario.setShowGrid(True)
        self.inventario.setGridStyle(QtCore.Qt.SolidLine)
        style = "QTableWidget { gridline-color: #e7eff7; background: none; color: rgb(70, 79, 78); padding: 2px;}"
        self.inventario.setStyleSheet(style)
        # botonbuscar
        self.pushButton_4.clicked.connect(self.actions_search)
        # boton de panel:
        self.panelControlButtom.clicked.connect(self.show_panel_frame)
        # Menu:
        self.show_items(_date)
        self.editarFrame.hide()
        self.editarFrame_2.hide()
        self.actualizarFrame.hide()
        self.eliminarFrame.hide()
        self.exelFrame.hide()
        #sub menu:
        self.date = []
        self.guardarBoton.clicked.connect(lambda: self.actions_upgrade(self.date.name_item, self.actualizarLine.text()))
        self._name = self.actualizarLine_3.text()
        self._unit = self.actualizarLine_4.text()
        self._quantity = self.actualizarLine_5.text()
        self._lot = self.actualizarLine_6.text()
        self._exp = self.actualizarLine_7.text()
        self.guardarBoton_3.clicked.connect(lambda: self.actions_upgrade_info(self.date.name_item))
        self.guardarBoton_4.clicked.connect(lambda: self.actions_add_exel(self.date.id))
        self.guardarBoton_5.clicked.connect(lambda: self.actions_delete(self.date.name_item))
        self.guardarBoton_6.clicked.connect(self.eliminarFrame.hide)
        self.guardarBoton_7.clicked.connect(self.actions_add_insumo)
        self.guardarBoton_8.clicked.connect(lambda: self.action_upgrade_info_exel(self.date.id))

    def mousePressEvent(self, event):
        self.aggFrame.hide()
        self.editarFrame.hide()
        self.editarFrame_2.hide()
        self.actualizarFrame.hide()
        self.eliminarFrame.hide()
        self.exelFrame.hide()

    def show_items(self, _dates):
        self.indicator = False
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
            self.inventario.setItem(index_a, 2, item_two)
            self.inventario.setItem(index_a, 1, item_tre)
            self.inventario.setItem(index_a, 3, item_four)
            self.inventario.setItem(index_a, 4, item_five)
            self.editarBoton = QtWidgets.QPushButton()
            self.editarBoton.setText("Editar")
            self.editarBoton.clicked.connect(lambda _, date = row,
                                            _pos = self.editarBoton.geometry().x() : self.show_edit_frame(date, _pos))
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

    def show_frames(self, pos_x, pos_y, date, limite, frame_show, tamx, tamy):
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
            # agregados:
            b = [date.name_item, date.unit, str(date.quantity), date.lot, str(date.exp)]
            linesEdit = [self.actualizarLine_3, self.actualizarLine_4, self.actualizarLine_5, self.actualizarLine_6,
                         self.actualizarLine_7]
            for index in range(5):
                if b[index] == '' or b[index] == 'None':
                    linesEdit[index].setText('')
                else:
                    linesEdit[index].setText(b[index])
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.information(self, "Inventario de Almacen", f"e")

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

    def show_panel_frame(self):
        self.editarFrame.hide()
        self.editarFrame_2.hide()
        self.actualizarFrame.hide()
        self.eliminarFrame.hide()
        self.exelFrame.hide()
        self.aggFrame.hide()
        log = Login()
        date = self.loop.run_until_complete(log.get_date())
        self.lineEdit.setText('')
        self.show_items(date)

    def show_edit_frame(self, date, _pos):
        try:
            self.date = date
            print(f"envio:{date.name_item}")
            buttom = self.sender()
            position = buttom.pos()

            if buttom and position.y() < 350:
                self.editarFrame.setGeometry(position.x()-45, position.y()+47, 111, 141)
                self.editarFrame.show()
            else:
                self.editarFrame.setGeometry(position.x()-45, 378, 111, 141)
                self.editarFrame.show()

            self.editarFrame_2.hide()
            self.actualizarFrame.hide()
            self.eliminarFrame.hide()
            self.exelFrame.hide()
            self.aggFrame.hide()

            self.actualizar.clicked.connect(lambda: self.show_frames(position.x()-45, position.y()+47, date,
                                        397, self.actualizarFrame, 301, 111))
            self.editar.clicked.connect(lambda: self.show_frames(position.x()-175, position.y()+47, date,
                                        250, self.editarFrame_2, 441, 271))
            self.eliminar.clicked.connect(lambda: self.show_frames(position.x()-45, position.y()+47, date,
                                        397, self.eliminarFrame, 301, 111))
            self.exel.clicked.connect(lambda: self.show_frames(position.x() - 45, position.y() + 47, date,
                                        308, self.exelFrame, 301, 211))
            #Agregado:
            indicador_exist = self.loop.run_until_complete(self._get_exel(date.id))
            if len(indicador_exist) == 0:
                self.actualizarLine_8.setText("")
                self.actualizarLine_9.setText("")
                self.actualizarLine_10.setText("")
                self.guardarBoton_7.show()
                self.guardarBoton_8.hide()
            else:
                ejem = indicador_exist[0]
                self.guardarBoton_8.show()
                self.guardarBoton_7.hide()
                self.actualizarLine_8.setText(ejem.name_docx_one)
                self.actualizarLine_9.setText(ejem.name_docx_two)
                self.actualizarLine_10.setText(ejem.name_docx_tre)
        except Exception as e:
            print(e)
            if str(e) != 'Event loop is closed':
                QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")

    def actions_search(self):
        try:
            text = self.lineEdit.text()
            boolean = self.loop.run_until_complete(self._search(text))
            if boolean == False:
                QtWidgets.QMessageBox.information(self, "Inventario de Almacen",
            "No se ha encontrado un insumo con esa descripcion")
            self.indicator = True
        except Exception as e:
            print(f"ERROR:{e}")

    def actions_upgrade(self, _name, _quantity):
        try:
            new_quantity = float(_quantity)
            self.loop.run_until_complete(self._upgrade(_name, new_quantity))
            log = Login()
            self.actualizarFrame.hide()
            self.actualizarLine.setText('')
            if self.indicator == False and self.lineEdit.text() == '':
                date = self.loop.run_until_complete(log.get_date())
                self.show_items(date)
            else:
                date = self.loop.run_until_complete(self.search(self.lineEdit.text()))
        except ValueError as e:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", "El valor no es un número válido")
        except Exception as e:
            print(f"ERROR_2: {e}")
            if str(e) != 'Event loop is closed':
                QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"{e}")

    def actions_upgrade_info(self, indx):
        try:
            c = [self.actualizarLine_3.text(), self.actualizarLine_5.text(), self.actualizarLine_4.text(),
                 self.actualizarLine_6.text(), self.actualizarLine_7.text()]
            c = self.func.group_list(c)
            self.loop.run_until_complete(self._upgrade_info( indx, c[0], c[1], c[2], c[3], c[4]))
            log = Login()
            self.editarFrame_2.hide()
            if self.indicator == False and self.lineEdit.text() == '':
                date = self.loop.run_until_complete(log.get_date())
                self.show_items(date)
            else:
                date = self.loop.run_until_complete(self.search(self.lineEdit.text()))
        except ValueError as e:
            print(f"ERRO_3: {e}")
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen",
            "El valor no es un número válido o una fecha valida.")
        except Exception as e:
            print(f"ERROR_2: {e}")
            if str(e) != 'Event loop is closed':
                QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"ERROR: {e}")

    def actions_delete(self, _name):
        try:
            self.loop.run_until_complete(self._delete(_name))
            log = Login()
            date = self.loop.run_until_complete(log.get_date())
            self.show_items(date)
            self.eliminarFrame.hide()
        except Exception as e:
            print(f"ERROR_2: {e}")

    def actions_add_insumo(self):
        try:
            c = [self.actualizarLine_11.text(), self.actualizarLine_13.text(), self.actualizarLine_12.text(),
                 self.actualizarLine_14.text(), self.actualizarLine_15.text()]
            c = self.func.group_list(c)
            self.loop.run_until_complete(self._add_insumo(c[0], c[1], c[2], c[3], c[4]))
            log = Login()
            date = self.loop.run_until_complete(log.get_date())
            self.aggFrame.hide()
            self.show_items(date)
        except Exception as e:
            print(f"ERRRORORORS: {e}")

    def actions_add_exel(self, _indx):
        try:
            c = [self.actualizarLine_8.text(), self.actualizarLine_9.text(), self.actualizarLine_10.text()]
            for index in range(2):
                if c[index] == "":
                    c[index] = None
            result = self.loop.run_until_complete(self._add_exel(_indx, c[0], c[1], c[2]))
            print(c[0])
            print(c[1])
            print(c[2])
            self.exelFrame.hide()
        except Exception as e:
            print(f'ErroExel1: {e}')

    def action_upgrade_info_exel(self, _id):
        try:
            self.loop.run_until_complete(self._upgrade_info_exel(_id, self.actualizarLine_8.text(),
                                                                 self.actualizarLine_9.text(),
                                                                 self.actualizarLine_10.text()))
            self.exelFrame.hide()
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen", f"ERROR: {e}")

    async def _search(self, _name_item):
        ii = ItemInventory()
        await init()
        result = await ii.get_ones_item(_name_item)
        await close()
        if result[0] != None:
            self.show_items(result)
            self.indicator = True
            return True
        else:
            return False

    async def _upgrade(self, _name, _quantity):
        self.indicator = False
        ii = ItemInventory()
        await init()
        await ii.update_item(_name, _quantity)
        await close()

    async def _upgrade_info(self, _indx, _name, _quantity, _unit, _lot, _exp):
        self.indicator = False
        a = [_name, _quantity, _unit, _lot, _exp]
        for argument in a:
            if argument == '':
                argument = None
        ii = ItemInventory()
        await init()
        await ii.update_info_item(_indx, _name, _quantity, _unit, _lot, _exp)
        await close()

    async def _delete(self, _name):
        ii = ItemInventory()
        await init()
        await ii.delete_item(_name)
        await close()

    async def _add_insumo(self, _name, _quantity, _unit, _lot, _exp):
        ii = ItemInventory()
        await init()
        verific = await ii.verific_exist(_name)
        if verific:
            await ii.add_item(_name, _quantity, _unit, _lot, _exp)
        else:
            QtWidgets.QMessageBox.information(self, "Sistema de Almacen",
            "Ya se encuentra un articulo con esta descripcion.")
        await close()

    async def _add_exel(self, _id, _name_doc1, _name_doc2, _name_doc3):
        ei = ExelInventory()
        await init()
        result = await ei.save_exel(_id, _name_doc1, _name_doc2, _name_doc3)
        print(f"aquiiii{result}")
        await close()

    async def _get_exel(self, _id):
        ei = ExelInventory()
        await init()
        result = await ei.get_name_exel(id=_id)
        await close()
        return result

    async def _upgrade_info_exel(self, _id, _name_doc1, _name_doc2, _name_doc3):
        ei = ExelInventory()
        await init()
        result = await ei.update_info_exel(_id, _name_doc1, _name_doc2, _name_doc3)
        await close()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        program = Login()
        program.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)