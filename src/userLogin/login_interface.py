from PyQt5 import QtCore, QtWidgets
from src.db.crud import UserLogin, ItemInventory
from src.db.__init__ import init, close
import asyncio

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(649, 447)
        Dialog.setWindowTitle("")
        Dialog.setStyleSheet("")
        self.PrimerFrame = QtWidgets.QFrame(Dialog)
        self.PrimerFrame.setGeometry(QtCore.QRect(0, 0, 651, 461))
        self.PrimerFrame.setMinimumSize(QtCore.QSize(651, 451))
        self.PrimerFrame.setStyleSheet("background-image: url(ivssLogin.png);")
        self.PrimerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.PrimerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.PrimerFrame.setObjectName("PrimerFrame")
        self.label = QtWidgets.QLabel(self.PrimerFrame)
        self.label.setGeometry(QtCore.QRect(410, 70, 171, 51))
        self.label.setStyleSheet("background: transparent;\n"
                                 "color: rgb(36, 70, 120);\n"
                                 "font: 87 16pt \"Arial\";\n"
                                 "border: none;")
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setIndent(0)
        self.label.setOpenExternalLinks(False)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.PrimerFrame)
        self.lineEdit.setGeometry(QtCore.QRect(400, 160, 191, 31))
        self.lineEdit.setStyleSheet("background : transparent;\n"
                                    "")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.PrimerFrame)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 250, 191, 31))
        self.lineEdit_2.setStyleSheet("background : transparent;\n"
                                      "")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.PrimerFrame)
        self.pushButton.setGeometry(QtCore.QRect(445, 320, 101, 41))
        self.pushButton.setStyleSheet("background: transparent;\n"
                                      "color: rgb(201, 222, 232);\n"
                                      "font: 75 10pt \"MS Shell Dlg 2\";\n"
                                      "background-color: rgb(62, 99, 148);\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.action)
        self.label_2 = QtWidgets.QLabel(self.PrimerFrame)
        self.label_2.setGeometry(QtCore.QRect(400, 140, 71, 21))
        self.label_2.setStyleSheet("background: transparent;\n"
                                   "font: 11pt \"MS Shell Dlg 2\";\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.PrimerFrame)
        self.label_3.setGeometry(QtCore.QRect(400, 220, 81, 21))
        self.label_3.setStyleSheet("background: transparent;\n"
                                   "font: 11pt \"MS Shell Dlg 2\";\n"
                                   "")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def action(self):
        asyncio.run(self.get_text())

    async def get_text(self):
        try:
            await init()
            _user = self.lineEdit.text()
            _password = self.lineEdit_2.text()
            lg = UserLogin()
            result = await lg.verific_user(_user, _password)
            if result:
                Dialog.close()
            else:
                QtWidgets.QMessageBox.information(Dialog, "Sistema de Almacen", "Acceso Denegado")
            await close()
        except Exception as e:
            QtWidgets.QMessageBox.information(Dialog, "Sistema de Almacen", f"{e}")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setWhatsThis(_translate("Dialog", "<html><head/><body><p>fsdfsd</p></body></html>"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#2c5b8b;\">Iniciar Sesion</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Iniciar Sesion"))
        self.label_2.setText(_translate("Dialog", "Usuario"))
        self.label_3.setText(_translate("Dialog", "Contraseña"))

    async def prueba(self):
        await init()
        ii = ItemInventory()
        await ii.add_item("bata", 15, "UNIDAD", "2121212")
        await close()

if __name__ == "__main__":
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    # ui.setupUi(Dialog)
    # Dialog.show()
    # sys.exit(app.exec_())

    asyncio.run(ui.prueba())

