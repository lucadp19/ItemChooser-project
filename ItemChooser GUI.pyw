from datetime import datetime, date, timedelta
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

import ItemChooser
import ICAnalyzer

from Msg import Msg
from TableWindows import AddTableWindow, RemoveTableWindow
from ItemsWindows import (InsertNewItemWindow, ChooseItemWindow, 
                         UpdateDateWindow, UpdatePriorityWindow)
from PrintingWindows import GenerateTableWindow, DataAnalysisWindow

# default login file
login_file = 'login_data.txt'

# [0]: Text of the buttons on the main windows
# [1]: name of the function that opens the new window
main_window_button_text = {
    'Insert new table': 'insert_new_table',
    'Remove a table': 'remove_table',
    'Insert new item': 'insert_new_item',
    'Choose a item': 'choose_item',
    'Update a item (date)': 'update_item_date',
    'Update a item (priority)': 'update_priority',
    'Print all the items': 'print_tables',
    'Run the data-analysis app': 'data_analysis',
    'Exit the application': 'exit_app'
}

# the algorithm for the database is the default one
algorithm = ItemChooser.default_algorithm


###################################################################
#                          LOGIN WINDOW                           #
###################################################################

class Ui_Dialog_LoginWindow(object):
    """Class built by QtDesigner for LoginWindow."""

    def setupUi(self, Dialog):
        """Defines the UI of LoginWindow().
        
        Arguments:
            Dialog {QtWidget.QDialog} -- parent object
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 251)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 231))
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
        self.inputUser = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputUser.setObjectName("inputUser")
        self.verticalLayout.addWidget(self.inputUser)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.inputPassw = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputPassw.setObjectName("inputPassw")
        self.verticalLayout.addWidget(self.inputPassw)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.inputDBName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputDBName.setObjectName("inputDBName")
        self.verticalLayout.addWidget(self.inputDBName)
        self.checkRemember = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkRemember.setObjectName("checkRemember")
        self.verticalLayout.addWidget(self.checkRemember)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "DATABASE LOGIN"))
        self.label_2.setText(_translate("Dialog", "Username:"))
        self.label_3.setText(_translate("Dialog", "Password:"))
        self.label_4.setText(_translate("Dialog", "Database name:"))
        self.checkRemember.setText(_translate("Dialog", "Remember this login"))


class LoginWindow(QtWidgets.QDialog, Ui_Dialog_LoginWindow, Msg):
    """Creates a window to login into a database. It is inizialized with
    the values for the login found in the text file; if there are none, 
    the values are set to ''.

    user is the username of the database.
    passw is the password of the database.
    db_name is the name of the database.
    parent is the parent widget, which defaults to None.
    """
    def __init__(self, user='', passw='', db_name='', parent=None):
        """Inizialises the LoginWindow with values for the login 
        found in the text file. If there are none, the values are
        set to ''.

        Keyword Arguments:
            user {str} -- database's username (default: {''})
            passw {str} -- database's password (default: {''})
            db_name {str} -- database's name (default: {''})
            parent {[type]} -- parent widget (default: {None})
        """
        super().__init__(parent)
        # Inizialises all the widgets in the window
        self.setupUi(self)

        # The three inputs have default values in them
        self.texts = [user, passw, db_name]
        self.inputUser.setText(self.texts[0])
        self.inputPassw.setText(self.texts[1])
        self.inputDBName.setText(self.texts[2])

        self.buttonBox.accepted.connect(self.tryLogin)
        self.buttonBox.rejected.connect(self.exitProcedure)

    def getLoginData(self):
        """To retrieve the information from the outside when the dialog is accepted.
        """
        user = self.inputUser.text()
        passw = self.inputPassw.text()
        db_name = self.inputDBName.text()

        login_data = [user, passw, db_name]

        return login_data

    def tryLogin(self):
        """Takes the values in the input lines and accepts the dialog.
        """
        user = self.inputUser.text()
        passw = self.inputPassw.text()
        db_name = self.inputDBName.text()
        printIt = self.checkRemember.isChecked()

        login_data = [user, passw, db_name]

        # If a field is empty
        if '' in login_data:
            msg = 'Every field must contain a value before trying to add the new value to the database.'
            self.criticalMsg(msg)
            self.resetFields()
            return None # interrupts the function

        # if the checkbox is checked it saves the data in login_file
        if printIt:
            with open(login_file, 'r+') as f:
                f.truncate(0)
                f.write('\n'.join([user, passw, db_name]))

        self.accept()

    def exitProcedure(self):
        self.reject()
    
    def resetFields(self):
        """Resets all the input fields.
        """
        self.inputUser.setText('')
        self.inputPassw.setText('')
        self.inputDBName.setText('')


###################################################################
#                          MAIN WINDOW                            #
###################################################################

class Window(QtWidgets.QWidget):
    """Main window. It presents a list of buttons with the database's functions;
    when a button is pressed a new space in the window appears, with the
    relative function. 

    user is the username of the database.
    passw is the password of the database.
    db_name is the name of the database.
    algorithm is the function that organizes the priority list based on date 
        and priority.
    """
    def __init__(self, user, passw, db_name, algorithm, ic_db=None):
        """Inizialises the database and the UI.
        
        Arguments:
            user {str} -- database's username
            passw {str} -- database's password
            db_name {str} -- database's name
            algorithm {function} -- function that organizes the priority list 
                                    based on date and priority

        Keyword Arguments:
            ic_db {ItemChooser.ItemChooser()} -- database already inizialised (default: {None})
        """
        super().__init__()
        # if no database has been given, use the credentials
        if ic_db is None:
            self.ic_db = ItemChooser.ItemChooser(user=user, passw=passw, db_name=db_name, algorithm=algorithm)
        else:
            self.ic_db = ic_db
        self.initUI()
        self.show()
    
    def initUI(self):
        """Inizialises the UI.
        """
        self.resize(250, 200)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                           QtWidgets.QSizePolicy.Fixed)
        #self.setFixedSize(1,1)

        # buttons' texts are contained in main_window_button_text
        buttons = [QtWidgets.QPushButton(button_text[0], self) 
            for button_text in main_window_button_text.items()]

        buttons_frame = QtWidgets.QWidget()
        buttons_layout = QtWidgets.QVBoxLayout()

        for button in buttons:
            # connects the button with the relative method
            method = self.button_method(main_window_button_text[button.text()])
            button.clicked.connect(method)
            buttons_layout.addWidget(button)

        buttons_frame.setLayout(buttons_layout)
        buttons_frame.setFixedWidth(200)

        hSpacing = QtWidgets.QSpacerItem(
            10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.box_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addItem(hSpacing)
        self.box_layout.addWidget(buttons_frame)
        self.box_layout.addItem(hSpacing)

        # currentLayout represents which function is active
        # At the beginning, no function is active so currentLayout = None
        self.currentLayout = None

        # nextLayout represents which function is about to be activated
        # At the beginning, no function is about to be activated so nextLayout = None
        self.nextLayout = None
        self.setLayout(self.box_layout)
    
    def changeLayouts(self):
        """changeLayouts manages the change between two different functions.
        """
        # If a function is currently active
        if self.currentLayout is not None:
            # close it
            # this triggers the resetView method
            self.currentLayout.close()
        else: # if no layout is currently active
            # nextLayout becomes currentLayout
            self.currentLayout = self.nextLayout
            self.nextLayout = None # no layout is waiting anymore
    
    def resetView(self):
        """Resets the window when a function is being closed.
        """
        # if resetView is triggered by exiting the function
        # so there is no layout waiting
        # reset to initial state
        if self.nextLayout is None:
            self.resize(250, 200)
            self.currentLayout = None # no function active anymore
        else: # if resetView is triggered by a new layout activating
            # nextLayout becomes currentLayout
            self.currentLayout = self.nextLayout
            self.nextLayout = None  # no layout is waiting anymore
    
    def button_method(self, button_text):
        """Generic button method, calls the particular method for each button.
        
        Arguments:
            button_text {str} -- text of the button, decides what function to call
        """
        method_name = 'button_{}'.format(button_text)
        # chooses the function
        method = getattr(self, method_name, self.generic_method)
        return method
    
    def generic_method(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText('Method not yet programmed!')
        msg.exec()

    def button_insert_new_table(self):
        """Function to insert a new table."""
        # Generates an AddTableWindow obj and puts it on "waiting" status
        newTable = AddTableWindow(self.ic_db)
        self.nextLayout = newTable

        # Changes the layout
        self.changeLayouts()
        
        self.resize(550, 200)
        self.box_layout.addWidget(newTable)

        # When the function is being closed, it calls resetView
        newTable.destroyed.connect(self.resetView)
    
    def button_remove_table(self):
        """Function to remove a table."""
        removeTable = RemoveTableWindow(self.ic_db)
        self.nextLayout = removeTable

        # Changes the layout
        self.changeLayouts()

        self.resize(550, 200)
        self.box_layout.addWidget(removeTable)

        # When the function is being closed, it calls resetView
        removeTable.destroyed.connect(self.resetView)

    def button_insert_new_item(self):
        """Function to insert a new item."""
        newItem = InsertNewItemWindow(self.ic_db)
        self.nextLayout = newItem

        # Changes the layout
        self.changeLayouts()
        
        self.resize(570, 300)
        self.box_layout.addWidget(newItem)

        # When the function is being closed, it calls resetView
        newItem.destroyed.connect(self.resetView)

    def button_choose_item(self):
        """Function to choose a random item."""
        chooseItem = ChooseItemWindow(self.ic_db)
        self.nextLayout = chooseItem

        # Changes the layout
        self.changeLayouts()

        self.resize(550, 200)
        self.box_layout.addWidget(chooseItem)

        # When the function is being closed, it calls resetView
        chooseItem.destroyed.connect(self.resetView)

    def button_update_item_date(self):
        """Function to update an item's date."""
        newDate = UpdateDateWindow(self.ic_db)
        self.nextLayout = newDate

        # Changes the layout
        self.changeLayouts()
        
        self.resize(570, 270)
        self.box_layout.addWidget(newDate)

        # When the function is being closed, it calls resetView
        newDate.destroyed.connect(self.resetView)
    
    def button_update_priority(self):
        """Function to update an item's priority."""
        newPriority = UpdatePriorityWindow(self.ic_db)
        self.nextLayout = newPriority

        # Changes the layout
        self.changeLayouts()
        
        self.resize(570, 270)
        self.box_layout.addWidget(newPriority)

        # When the function is being closed, it calls resetView
        newPriority.destroyed.connect(self.resetView)
    
    def button_print_tables(self):
        """Function to print the entirety of a table."""
        generateTable = GenerateTableWindow(self.ic_db)
        self.nextLayout = generateTable

        # Changes the layout
        self.changeLayouts()
        
        self.resize(670, 320)
        self.box_layout.addWidget(generateTable)

        # When the function is being closed, it calls resetView
        generateTable.destroyed.connect(self.resetView)
    
    def button_data_analysis(self):
        """Function to do data-analysis."""
        generateAnalysis = DataAnalysisWindow(self.ic_db)
        self.nextLayout = generateAnalysis

        # Changes the layout
        self.changeLayouts()

        self.resize(620, 320)
        self.box_layout.addWidget(generateAnalysis)

        # When the function is being closed, it calls resetView
        generateAnalysis.destroyed.connect(self.resetView)
    
    def button_exit_app(self):
        """Function to exit the program."""
        sys.exit()

###################################################################
#                        MAIN APPLICATION                         #
###################################################################


def get_login_data(user='', passw='', db_name=''):
    """Creates a dialog to get the login's credentials.
    
    Keyword Arguments:
        user {str} -- database's username (default: {''})
        passw {str} -- database's password (default: {''})
        db_name {str} -- database's name (default: {''})
    """
    loginWindow = LoginWindow(user, passw, db_name)
    # if the dialog gets accepted
    if loginWindow.exec_() == QtWidgets.QDialog.Accepted:
        # it gets the login credentials
        login_data = loginWindow.getLoginData()
        return login_data

def main():
    """Main app: gets the credentials and creates the main window."""
    app = QtWidgets.QApplication(sys.argv)

    # takes the saved data from login_file
    with open(login_file, 'r+') as f:
        data = f.read()
        # if the file is empty
        if not data:
            # every field is empty
            user = passw = db_name = ''
        else:
            # otherwise it gets filled with the default values
            user, passw, db_name = data.split('\n')
        user, passw, db_name = get_login_data(user, passw, db_name)
    
    # main window
    window = Window(user, passw, db_name, algorithm)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

