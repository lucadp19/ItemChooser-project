from PyQt5 import QtCore, QtGui, QtWidgets

class Msg():
    """Defines two methods to print messages through QMessageBox."""
    def criticalMsg(self, error_msg):
        """Creates a QMessageBox with an error message.
        
        Arguments:
            error_msg {str} -- message to show
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(error_msg)
        msg.exec()

    def successfulMsg(self, succ_msg):
        """Creates a QMessageBox with an message indicating success.
        
        Arguments:
            succ_msg {str} -- message to show
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle('Successful')
        msg.setText(succ_msg)
        msg.exec()
