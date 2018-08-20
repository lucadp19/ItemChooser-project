import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import ItemChooser
from Msg import Msg


###################################################################
#                       INSERT TABLE WINDOW                       #
###################################################################


class Ui_Form_AddTable(object):
    """Class built by QtDesigner for AddTableWindow."""

    def setupUi(self, Form):
        """Defines the UI of AddTableWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(280, 132)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 281, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.inputTableName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputTableName.setObjectName("inputTableName")
        self.verticalLayout.addWidget(self.inputTableName)
        spacerItem = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonAdd = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonAdd.setObjectName("buttonAdd")
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.buttonExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout.addWidget(self.buttonExit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "ADD TABLE"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.buttonAdd.setText(_translate("Form", "Add"))

        self.buttonExit.setText(_translate("Form", "Exit"))


class AddTableWindow(QtWidgets.QWidget, Ui_Form_AddTable, Msg):
    """Widget whose function is to add a table to the database.
    
    ic_db is an instance of ItemChooser(). It represents the database on which
    the actions will be performed.
    
    parent is the parent widget, which defaults to None."""
    def __init__(self, ic_db, parent=None):
        """Initializes the window with all of the necessary information.
        
        Arguments:
            ic_db {ItemChooser()} -- ItemChooser object which contains the database
        
        Keyword Arguments:
            parent {QtWidget.QWidget} -- parent widget (default: {None})
        """

        # Inizialises the UI
        super().__init__(parent)
        self.setupUi(self)

        self.ic_db = ic_db
        self.buttonAdd.clicked.connect(self.addTable)
        self.buttonExit.clicked.connect(self.close)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def addTable(self):
        """Adds a new table to the database."""
        table_name = self.inputTableName.text()

        try:
            self.ic_db.add_new_table(table_name)
            self.successfulMsg('Table added!')
        except Exception as e:
            self.criticalMsg(str(e))
        finally:
            self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        self.inputTableName.setText('')


###################################################################
#                       REMOVE TABLE WINDOW                       #
###################################################################


class Ui_Form_RemoveTable(object):
    """Class built by QtDesigner for RemoveTableWindow."""

    def setupUi(self, Form):
        """Defines the UI of RemoveTableWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(280, 132)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 281, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.inputTableName = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.inputTableName.setObjectName("inputTableName")
        self.verticalLayout.addWidget(self.inputTableName)
        spacerItem = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonRemove = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonRemove.setObjectName("buttonRemove")
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.buttonExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout.addWidget(self.buttonExit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "REMOVE TABLE"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.buttonRemove.setText(_translate("Form", "Remove"))
        self.buttonExit.setText(_translate("Form", "Exit"))


class RemoveTableWindow(QtWidgets.QWidget, Ui_Form_RemoveTable, Msg):
    """Widget whose function is to remove a table from the database.
    
    ic_db is an instance of ItemChooser(). It represents the database on which
    the actions will be performed.
    
    parent is the parent widget, which defaults to None."""
    def __init__(self, ic_db, parent=None):
        """Initializes the window with all of the necessary information.
        
        Arguments:
            ic_db {ItemChooser()} -- ItemChooser object which contains the database
        
        Keyword Arguments:
            parent {QtWidget.QWidget} -- parent widget (default: {None})
        """

        # Inizialises the UI
        super().__init__(parent)
        self.setupUi(self)

        self.ic_db = ic_db
        self.buttonRemove.clicked.connect(self.removeTable)
        self.buttonExit.clicked.connect(self.close)
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        

    def removeTable(self):
        """Removes a table from the database."""
        table_name = self.inputTableName.currentText()

        try:
            # checks to be sure
            msg = QtWidgets.QMessageBox.question(
                self, 'Removing table',
                'Do you really want to remove "{}" table?'.format(table_name),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if msg == QtWidgets.QMessageBox.Yes:
                self.successfulMsg('Table removed!')
                self.ic_db.remove_table(table_name)
        except Exception as e:
            self.criticalMsg(str(e))
        finally:
            self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)
