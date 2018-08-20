from PyQt5 import QtCore, QtGui, QtWidgets
import ItemChooser
import ICAnalyzer
from Msg import Msg


###################################################################
#                         PRINTING TABLES                         #
###################################################################


class Ui_Form_GenerateTable(object):
    """Class built by QtDesigner for GenerateTableWindow."""

    def setupUi(self, Form):
        """Defines the UI of GenerateTableWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(420, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 400, 291))
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.buttonGroup = QtWidgets.QButtonGroup(self.verticalLayoutWidget)
        self.checkSortedByDate = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkSortedByDate.setObjectName("checkSortedByDate")
        self.buttonGroup.addButton(self.checkSortedByDate)
        self.verticalLayout_2.addWidget(self.checkSortedByDate)
        self.checkSortedByPriority = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        self.checkSortedByPriority.setObjectName("checkSortedByPriority")
        self.buttonGroup.addButton(self.checkSortedByPriority)
        self.verticalLayout_2.addWidget(self.checkSortedByPriority)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.buttonPrint = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonPrint.setObjectName("buttonPrint")
        self.horizontalLayout_4.addWidget(self.buttonPrint)
        self.buttonExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout_4.addWidget(self.buttonExit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)

        # no item editing
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        # table headers
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ITEMS', 'DATE', 'PRIORITY'])

        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "GENERATE TABLES"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Sorted by:"))
        self.checkSortedByDate.setText(_translate("Form", "DATE"))
        self.checkSortedByPriority.setText(_translate("Form", "PRIORITY"))
        self.buttonPrint.setText(_translate("Form", " Generate table "))
        self.buttonExit.setText(_translate("Form", "Exit"))


class GenerateTableWindow(QtWidgets.QWidget, Ui_Form_GenerateTable, Msg):
    """Widget whose function is to show the database's tables.
    
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
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)
        self.buttonPrint.clicked.connect(self.generate)
        self.buttonExit.clicked.connect(self.close)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def generate(self):
        """Shows a table from the database."""
        table_name = self.inputTableName.currentText()
        sorted_by_date = self.checkSortedByDate.isChecked()
        sorted_by_priority = self.checkSortedByPriority.isChecked()

        # check if the table is empty
        try:
            self.ic_db.check_if_table_empty(table_name)
        except ItemChooser.DatabaseException as e:
            self.criticalMsg(str(e))
            return None

        # dataframe containing all data from a table
        df = self.ic_db.print_table(table_name, sorted_by_date=sorted_by_date,
                                 sorted_by_priority=sorted_by_priority, tabulate=False)

        # clear tableWidget
        self.tableWidget.setRowCount(0)

        # add items one at a time
        currentRow = self.tableWidget.rowCount()
        for elem in df:
            self.tableWidget.insertRow(currentRow)
            for i in range(len(elem)):
                self.tableWidget.setItem(
                    currentRow, i,
                    QtWidgets.QTableWidgetItem(
                        str(elem[i]) if i != 1 else str(elem[i].date()))
                )
            currentRow = self.tableWidget.rowCount()
        self.tableWidget.resizeColumnsToContents()


###################################################################
#                         DATA-ANALYSIS                           #
###################################################################


class Ui_Form_DataAnalysis(object):
    """Class built by QtDesigner for DataAnalysisWindow."""

    def setupUi(self, Form):
        """Defines the UI of DataAnalysisWindow.
        
        Arguments:
            Form {QtWidgets.QWidget} -- parent widget
        """
        Form.setObjectName("Form")
        Form.resize(361, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 341, 291))
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

        self.repCounter = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.repCounter.setMinimum(1)
        self.repCounter.setMaximum(999999)
        self.repCounter.setProperty("value", 1000)
        self.repCounter.setObjectName("repCounter")
        self.verticalLayout.addWidget(self.repCounter)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.buttonGenerate = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonGenerate.setObjectName("buttonGenerate")
        self.horizontalLayout_4.addWidget(self.buttonGenerate)
        self.buttonExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout_4.addWidget(self.buttonExit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)

        # no item editing
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        # set table's headers
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ITEMS', 'REPS', 'DATE', 'PRIORITY'])
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "DATA-ANALYSIS APPLICATION"))
        self.label_2.setText(_translate("Form", "Table name:"))
        self.label_3.setText(_translate("Form", "Number of items chosen:"))
        self.buttonGenerate.setText(_translate("Form", " Generate table "))
        self.buttonExit.setText(_translate("Form", "Exit"))


class DataAnalysisWindow(QtWidgets.QWidget, Ui_Form_DataAnalysis, Msg):
    """Analyses data from the database. After choosing a table and a repetition
    counter, it calls the choose_dish rep_counter times and saves the result.
    Then it shows it in tabular form.
    
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
        self.buttonGenerate.clicked.connect(self.generateAnalysis)
        self.buttonExit.clicked.connect(self.close)
        self.inputTableName.clear()
        self.inputTableName.addItems(self.ic_db._TABLE_NAMES_LIST)

        # When closed, it's immediately destroyed
        # in order to change layouts correctly
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def generateAnalysis(self):
        """Calls the choose_dish function rep_limit times and generates a table
        with the results."""
        table_name = self.inputTableName.currentText()
        rep_limit = self.repCounter.value()

        analyzer = ICAnalyzer.ItemChooserAnalyzer(ic_db=self.ic_db)

        try:
            df = analyzer.run(table_name=table_name, rep_limit=rep_limit,
                              tabulate=False)
        # if the table is empty
        except ItemChooser.DatabaseException as e:
            self.criticalMsg(str(e))
            return None

        # clear tableWidget
        self.tableWidget.setRowCount(0)

        # adds items one at a time
        currentRow = self.tableWidget.rowCount()
        for elem in df:
            self.tableWidget.insertRow(currentRow)
            for i in range(len(elem)):
                self.tableWidget.setItem(
                    currentRow, i,
                    QtWidgets.QTableWidgetItem(str(elem[i]))
                )
            currentRow = self.tableWidget.rowCount()
        self.tableWidget.resizeColumnsToContents()
