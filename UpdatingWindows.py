from datetime import datetime, date, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import ItemChooser
from Msg import Msg


###################################################################
#                       CHOOSE ITEM WINDOW                        #
###################################################################


class Ui_Form_ChooseItem(object):
    """Class built by QtDesigner for ChooseItemWindow."""

    def setupUi(self, Form):
        """Defines the UI of ChooseItemWindow.

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
        self.buttonSearch = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonSearch.setObjectName("buttonSearch")
        self.horizontalLayout.addWidget(self.buttonSearch)
        self.buttonExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout.addWidget(self.buttonExit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "CHOOSE ITEM"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.buttonSearch.setText(_translate("Form", "Search"))
        self.buttonExit.setText(_translate("Form", "Exit"))


class ChooseItemWindow(QtWidgets.QWidget, Ui_Form_ChooseItem, Msg):
    """Widget whose function is to choose a random item from the database.
    
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
        self.buttonSearch.clicked.connect(self.choiceSearch)
        self.buttonExit.clicked.connect(self.close)
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def choiceSearch(self):
        """Chooses a random item from the database."""
        table_name = self.inputTableName.currentText()

        try:  # if table is not empty
            self.ic_db.check_if_table_empty(table_name)
        except ItemChooser.DatabaseException as e:
            self.criticalMsg(str(e))
            self.resetFields()
            return None

        try:
            # gets the dataframe
            df = self.ic_db.get_dataframe(table_name)
        except ItemChooser.TableNameException as e:
            self.criticalMsg(str(e))
            self.resetFields()
        else:
            # while the user doesn't choose an item
            while True:
                choice = self.ic_db.choose_item(table_name, df)
                # ask if accepted
                buttonReply = QtWidgets.QMessageBox.question(
                    self,
                    'Accept choice',
                    'Do you want to accept this choice: "{}"?'.format(
                        choice),
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                    QtWidgets.QMessageBox.No,
                )
                # if accepted
                if buttonReply == QtWidgets.QMessageBox.Yes:
                    try:
                        # update the date to today
                        self.ic_db.update_item_date(table_name, choice)
                        self.successfulMsg('Data updated!')
                        break
                    except Exception as e:
                        self.criticalMsg(str(e))
                        self.resetFields()
                # if not accepted
                elif buttonReply == QtWidgets.QMessageBox.No:
                    pass  # continue
                # if canceled break
                elif buttonReply == QtWidgets.QMessageBox.Cancel:
                    break

    def resetFields(self):
        """Resets all fields of the widget."""
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)


###################################################################
#                       UPDATE ITEM WINDOW                        #
###################################################################


class Ui_Form_UpdateDate(object):
    """Class built by QtDesigner for UpdateDateWindow.
    
    ic_db is an instance of ItemChooser(). It represents the database on which
    the actions will be performed.
    
    parent is the parent widget, which defaults to None."""

    def setupUi(self, Form):
        """Defines the UI of UpdateDateWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(300, 240)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 301, 231))
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
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.inputNewDate = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.inputNewDate.setObjectName("inputNewDate")
        # default date is today
        self.inputNewDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.verticalLayout.addWidget(self.inputNewDate)

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
        self.label.setText(_translate("Form", "UPDATE ITEM DATE"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Item name:"))
        self.label_4.setText(_translate("Form", "New date:"))


class UpdateDateWindow(QtWidgets.QWidget, Ui_Form_UpdateDate, Msg):
    """Widget whose function is to update the date of an item from the database.
    
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
        self.buttonBox.accepted.connect(self.updateDate)
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

    def updateDate(self):
        """Updates the date of an item from the database."""
        table_name = self.inputTableName.currentText()
        item_name = self.inputItemName.currentText()
        item_date = self.inputNewDate.dateTime().toPyDateTime()

        # if a field is empty
        if '' in [table_name, item_name]:
            msg = ("Every field must contain a value before trying "
                   "to add the new value to the database")
            self.criticalMsg(msg)
        else:
            try:
                self.ic_db.update_item_date(
                    table_name=table_name,
                    item_name=item_name,
                    new_date=item_date,
                )
                self.successfulMsg('Update succeded!')
            except ItemChooser.DatabaseException as e:
                self.criticalMsg(str(e))
            except ItemChooser.TableNameException as e:
                self.criticalMsg(str(e))

        self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        # this automatically resets inputItemName as well
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        self.inputNewDate.setDateTime(QtCore.QDateTime.currentDateTime())


###################################################################
#                     UPDATE PRIORITY WINDOW                      #
###################################################################


class Ui_Form_UpdatePriority(object):
    """Class built by QtDesigner for UpdatePriorityWindow."""

    def setupUi(self, Form):
        """Defines the UI of UpdatePriorityWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(298, 229)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 301, 231))
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
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.inputNewPriority = QtWidgets.QDoubleSpinBox(
            self.verticalLayoutWidget)

        self.inputNewPriority.setObjectName("inputNewPriority")
        self.inputNewPriority.setValue(1.0)
        self.inputNewPriority.setSingleStep(0.1)
        self.inputNewPriority.setMinimum(0.1)
        self.inputNewPriority.setMaximum(10)
        self.verticalLayout.addWidget(self.inputNewPriority)

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
        self.label.setText(_translate("Form", "UPDATE ITEM PRIORITY"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Item name:"))
        self.label_4.setText(_translate("Form", "New priority:"))


class UpdatePriorityWindow(QtWidgets.QWidget, Ui_Form_UpdatePriority, Msg):
    """Widget whose function is to update the priority of an 
    item from the database.
    
    ic_db is an instance of ItemChooser(). It represents the database on which
    the actions will be performed.
    
    parent is the parent widget, which defaults to None.
    """

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
        self.buttonBox.accepted.connect(self.updatePriority)
        self.buttonBox.rejected.connect(self.close)

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

    def updatePriority(self):
        """Updates the priority of an item from the database."""
        table_name = self.inputTableName.currentText()
        item_name = self.inputItemName.currentText()
        item_priority = self.inputNewPriority.value()

        # if a field is empty
        if '' in [table_name, item_name]:
            msg = ("Every field must contain a value before trying "
                   "to add the new value to the database")
            self.criticalMsg(msg)
        else:
            try:
                self.ic_db.update_priority(
                    table_name=table_name,
                    item_name=item_name,
                    new_priority=item_priority,
                )
                self.successfulMsg('Update successful!')
            except ItemChooser.DatabaseException as e:
                self.criticalMsg(str(e))
            except ItemChooser.TableNameException as e:
                self.criticalMsg(str(e))

        self.resetFields()

    def resetFields(self):
        """Resets all fields of the widget."""
        # this automatically resets inputItemName as well
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        self.inputNewPriority.setValue(1.0)
