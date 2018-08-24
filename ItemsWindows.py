from datetime import datetime, date, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import ItemChooser
from Msg import Msg

###################################################################
#                       INSERT ITEM WINDOW                        #
###################################################################


class Ui_Form_InsertNewItem(object):
    """Class built by QtDesigner for AddTableWindow."""

    def setupUi(self, Form):
        """Defines the UI of InsertNewItemWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(200, 200)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 300, 250))
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
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.inputItemName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputItemName.setObjectName("inputItemName")
        self.verticalLayout.addWidget(self.inputItemName)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.inputDate = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.inputDate.setObjectName("inputDate")
        # default date is today
        self.inputDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.verticalLayout.addWidget(self.inputDate)

        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)

        self.inputPriority = QtWidgets.QDoubleSpinBox(
            self.verticalLayoutWidget)
        self.inputPriority.setSingleStep(0.1)
        self.inputPriority.setValue(1.0)
        self.inputPriority.setMinimum(0.1)
        self.inputPriority.setMaximum(10)
        self.inputPriority.setObjectName("inputPriority")
        self.verticalLayout.addWidget(self.inputPriority)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "INSERT NEW DISH"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Item name:"))
        self.label_4.setText(_translate("Form", "Date:"))
        self.label_5.setText(_translate("Form", "Priority:"))


class InsertNewItemWindow(QtWidgets.QWidget, Ui_Form_InsertNewItem, Msg):
    """Widget whose function is to add an item to the database.
    
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
        self.buttonBox.accepted.connect(self.insertItem)
        self.buttonBox.rejected.connect(self.close)
        
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def insertItem(self): 
        """Inserts a new item to the database."""
        # gets the data from the window
        table_name = self.inputTableName.currentText()
        item_name = self.inputItemName.text()
        item_date = self.inputDate.dateTime().toPyDateTime()
        item_priority = self.inputPriority.value()

        # if there is an empty field
        if '' in [table_name, item_name]:
            msg = 'Every field must contain a value before trying to add the new value to the database.'
            self.criticalMsg(msg)
        else:
            try:
                self.ic_db.insert_new_item(
                    table_name=table_name,
                    item_name=item_name,
                    item_date=item_date,
                    item_priority=item_priority,
                )
                self.successfulMsg('Insertion succeded!')
            except ItemChooser.TableNameException as e:
                self.criticalMsg(str(e))
        self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        self.inputItemName.setText('')
        self.inputDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.inputPriority.setValue(1.0)


###################################################################
#                       REMOVE ITEM WINDOW                        #
###################################################################


class Ui_Form_RemoveItem(object):
    """Class built by QtDesigner for AddTableWindow."""

    def setupUi(self, Form):
        """Defines the UI of InsertNewItemWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(200, 200)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 150))
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
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.inputItemName = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.inputItemName.setObjectName("inputItemName")
        self.verticalLayout.addWidget(self.inputItemName)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "REMOVE ITEM"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Item name:"))


class RemoveItemWindow(QtWidgets.QWidget, Ui_Form_RemoveItem, Msg):
    """Widget whose function is to remove an item from the database.
    
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
        self.buttonBox.accepted.connect(self.removeItem)
        self.buttonBox.rejected.connect(self.close)

        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        # inputItemName field is filled with all the items from the selected table
        self.updateItems()
        # when the table changes, the inputItemName field is updated
        # thanks to the function updateItems
        self.inputTableName.currentIndexChanged.connect(self.updateItems)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def updateItems(self):
        """Fills the inputItemName field with all the items in the current table."""
        current_table_name = self.inputTableName.currentText()

        try:  # if the table is empty
            self.ic_db.check_if_table_empty(current_table_name)
        except:  # the inputItemName field is empty too
            self.inputItemName.clear()
        else:
            # select every name from the table
            cursor = self.ic_db.db.cursor()
            cursor.execute('SELECT name FROM {}'.format(current_table_name))

            # add every item to inputItemName
            self.inputItemName.clear()
            for elem in cursor.fetchall():
                self.inputItemName.addItem(elem[0])

            cursor.close()

    def removeItem(self):
        """Removes an item from the database."""
        # gets the data from the window
        table_name = self.inputTableName.currentText()
        item_name = self.inputItemName.currentText()

        # if there is an empty field
        if '' in [table_name, item_name]:
            msg = 'Every field must contain a value before trying to remove the item from the database.'
            self.criticalMsg(msg)
        else:
            # checks to be sure
            msg = QtWidgets.QMessageBox.question(
                self, 'Removing table',
                'Do you really want to remove this item: "{}"?'.format(
                    item_name),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if msg == QtWidgets.QMessageBox.Yes:
                try:
                    self.ic_db.remove_item(
                        table_name=table_name,
                        item_name=item_name,
                    )
                    self.successfulMsg('Insertion succeded!')
                except ItemChooser.TableNameException as e:
                    self.criticalMsg(str(e))
        self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        # this automatically resets inputItemName as well
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)
