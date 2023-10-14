import sys
import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent

from Navigation import Ui_MainWindow
import resource_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)

        self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.statistik.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.impotPage)))
        self.ui.qrGenBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
