from PyQt6 import QtCore, QtGui, QtWidgets


class new_delete_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(362, 300)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.complitedBox = QtWidgets.QComboBox(parent=Dialog)
        self.complitedBox.setObjectName("complitedBox")
        self.complitedBox.addItem("")
        self.complitedBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.complitedBox)
        self.priorityBox = QtWidgets.QComboBox(parent=Dialog)
        self.priorityBox.setObjectName("priorityBox")
        self.priorityBox.addItem("")
        self.priorityBox.addItem("")
        self.priorityBox.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.priorityBox)
        self.contentEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.contentEdit.setObjectName("contentEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.contentEdit)
        self.applyButton = QtWidgets.QPushButton(parent=Dialog)
        self.applyButton.setObjectName("ApplyButton")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.applyButton)
        self.timeEdit = QtWidgets.QTimeEdit(parent=Dialog)
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.timeEdit)
        self.dateEdit = QtWidgets.QDateEdit(parent=Dialog)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.dateEdit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Иструменты"))
        self.label.setText(_translate("Dialog",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Сохранение/Изменение</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Выполнена?"))
        self.complitedBox.setItemText(0, _translate("Dialog", "NO"))
        self.complitedBox.setItemText(1, _translate("Dialog", "YES"))
        self.priorityBox.setItemText(0, _translate("Dialog", "Lite"))
        self.priorityBox.setItemText(1, _translate("Dialog", "Medium"))
        self.priorityBox.setItemText(2, _translate("Dialog", "Hard"))
        self.applyButton.setText(_translate("Dialog", "Применить"))


class search_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 200)
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(20, 20, 200, 30))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.contentEdit = QtWidgets.QLineEdit(Dialog)
        self.contentEdit.setGeometry(QtCore.QRect(20, 70, 350, 30))
        self.contentEdit.setPlaceholderText("Введите текст для поиска")
        self.contentEdit.setObjectName("contentEdit")
        self.searchButton = QtWidgets.QPushButton(Dialog)
        self.searchButton.setGeometry(QtCore.QRect(50, 140, 100, 30))
        self.searchButton.setObjectName("searchButton")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(200, 140, 100, 30))
        self.cancelButton.setObjectName("cancelButton")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.move(228, 30)
        self.checkBox.setObjectName('checkBox')
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName('label')
        self.label.move(250, 28)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Поиск заметок"))
        self.searchButton.setText(_translate("Dialog", "Найти"))
        self.cancelButton.setText(_translate("Dialog", "Отмена"))
        self.label.setText("Поиск по дате")
