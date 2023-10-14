import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent

from CustomTitleBar import CustomTitleBar

"""
Robotic Laborstraße GUI Project - Component

This code is a part of the Bachelor's thesis authored by Ujwal Subedi, conducted under the supervision of Prof. Adrian Müller at Hochschule Kaiserslautern.

Author: Ujwal Subedi
Date: 14.10.2023
"""

class HomePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is the Home Panel"))
        self.setStyleSheet("background-color:#FCC")

class StatistikenPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is the Statistiken Panel"))
        self.setStyleSheet("background-color:#FEE")

class ImportPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is the Import Panel"))
        self.setStyleSheet("background-color:#FCEFB1")

class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is the Settings Panel"))
        self.setStyleSheet("background-color:#FF00CC")

class LeftNavigation(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.initUI()
        self.setObjectName("leftNavigationMenu")        

    def connect_signals(self):
        self.buttons["Home"].clicked.connect(self.show_home_panel)
        self.buttons["Statistiken"].clicked.connect(self.show_statistiken_panel)
        self.buttons["Import"].clicked.connect(self.show_import_panel)
        self.buttons["Settings"].clicked.connect(self.show_settings_panel)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        

        # Mapping of menu items to their respective icons
        menu_items_icons = {
            "Home": "img/home.svg",
            "Statistiken": "img/graph-up.svg",
            "Import": "img/import-1.svg",
            "Settings": "img/settings.svg"
        }

         # Stores the created buttons
        self.buttons = {}  # Using a dictionary to store buttons by their names

        for item, icon_path in menu_items_icons.items():
            panel = QWidget(self)
            panel_layout = QVBoxLayout(panel)
            panel_layout.setContentsMargins(0, 0, 0, 0)
            panel.setObjectName(item)
            btn = QPushButton("")
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(32, 32))
            btn.setFixedSize(40, 40)
            btn.setObjectName(item)  # Sets the object name to the button
            btn.setToolTip(item)
            btn.enterEvent = lambda event, b=btn, i=item: self.show_text_on_hover(b, i)
            btn.leaveEvent = lambda event, b=btn: self.hide_text_on_hover(b)
            layout.addWidget(btn)
            self.buttons[item] = btn  # Adds the button to the dictionary

        self.connect_signals()

    def show_home_panel(self):
        self.main_window.home_panel.show()
        self.main_window.statistiken_panel.hide()  
        self.main_window.import_panel.hide()  
        self.main_window.settings_panel.hide()

    def show_statistiken_panel(self):
        self.main_window.home_panel.hide()
        self.main_window.statistiken_panel.show()
        self.main_window.import_panel.hide()  
        self.main_window.settings_panel.hide()

    def show_import_panel(self):
        self.main_window.home_panel.hide()
        self.main_window.statistiken_panel.hide()
        self.main_window.import_panel.show()  
        self.main_window.settings_panel.hide()

    def show_settings_panel(self):
        self.main_window.home_panel.hide()
        self.main_window.statistiken_panel.hide()
        self.main_window.import_panel.hide()  
        self.main_window.settings_panel.show()


    def show_text_on_hover(self, btn, item):
        # btn.setText(item)
        btn.setFixedSize(40, 40)

    def hide_text_on_hover(self, btn):
        btn.setText("")
        btn.setFixedSize(40, 40)


class StyledDashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Dashboard GUI")
        self.setGeometry(100, 100, 800, 600)

        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)

        # Make the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.home_panel = HomePanel(self)
        self.statistiken_panel = StatistikenPanel(self)
        self.import_panel = ImportPanel(self)
        self.settings_panel = SettingsPanel(self)

        # Create central widget and layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create main content layout
        content_layout = QHBoxLayout()
        left_nav = LeftNavigation(self)
        content_layout.addWidget(left_nav)
        self.create_live_view(content_layout)
        main_layout.addLayout(content_layout)

        main_layout.addWidget(self.home_panel)
        main_layout.addWidget(self.statistiken_panel)
        main_layout.addWidget(self.import_panel)
        main_layout.addWidget(self.settings_panel)

        #hide all panels
        self.home_panel.show()
        self.statistiken_panel.hide()
        self.import_panel.hide()
        self.settings_panel.hide()

        # Apply Stylesheet
        self.apply_stylesheet()

    def create_live_view(self, main_layout):
        live_view_layout = QVBoxLayout()

        # Create and add your panels here
        live_data_panel = LiveDataPanel(self)
        live_view_layout.addWidget(live_data_panel)
        live_view_layout.setObjectName("live_panel")

        main_layout.addLayout(live_view_layout, stretch=3)

    def apply_stylesheet(self):
        with open('stylesheet/stylen.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

class LiveDataPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        live_data_label = QLabel("Live Data Placeholder")
        layout.addWidget(live_data_label)


        # Add HomePanel
        home_panel = HomePanel(self)
        layout.addWidget(home_panel)

        # Add StatistikenPanel
        statistiken_panel = StatistikenPanel(self)
        layout.addWidget(statistiken_panel)

        # Add ImportPanel
        import_panel = ImportPanel(self)
        layout.addWidget(import_panel)

        # Add SettingsPanel
        settings_panel = SettingsPanel(self)
        layout.addWidget(settings_panel)

        self.setObjectName("liveDataPanel")

def run_app():
    app = QApplication(sys.argv)
    mainWin = StyledDashboardApp()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
