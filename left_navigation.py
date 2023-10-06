from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                            QWidget, QPushButton, QTextEdit,QTableWidget, QTabWidget)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from statistics_window import StatisticsWindow

from utils import Utils

class LeftNavigation(QWidget):
    def __init__(self, parent=None):
        super(LeftNavigation, self).__init__(parent)
        self.list_widget = QListWidget(self)
        self.right_panel = QVBoxLayout(self)
        self.__home_logo = "img/home.svg"
        self.__laboratory_logo = "img/laboratory.svg"
        self.__stream_logo = "img/stream.svg"
        self.import_panel = self.create_import_panel()
        self.home_panel = self.create_home_panel()
        self.statistics_panel = self.create_statistics_panel()
        self.setLayout(self._init_ui())
        
    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._create_logo(self.__laboratory_logo))
        self.list_widget.setFixedWidth(60)
        self.list_widget.minimumHeight = 60
        layout.addWidget(self.list_widget)
        return layout

    def _create_logo(self, logo_url):
        logo_label = QLabel()
        logo_label.setPixmap(Utils.get_pixmap_from_url(logo_url).scaledToWidth(50))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        # logo_label.setStyleSheet("margin-left:10px;margin-top:10px;max-width:50px;")
        return logo_label

    def create_import_panel(self):
        import_panel = QWidget()
        import_layout = QVBoxLayout(import_panel)
        import_layout.addWidget(QTextEdit("Import Panel Content"))
        return import_panel

    def create_statistics_panel(self):
        statistics_panel = QWidget()
        statistics_layout = QVBoxLayout(statistics_panel)
        statistics_layout.addWidget(QTextEdit("Statistics Panel Content"))
        return statistics_panel

    
    
    def on_item_clicked(self, item):
        for i in reversed(range(self.right_panel.count())): 
            self.right_panel.itemAt(i).widget().setParent(None)

        if item.text() == 'Home':
            print("home btn clicked")
            self.right_panel.addWidget(self.home_panel)
        elif item.text() == 'Import':
            print("import btn clicked")
            self.right_panel.addWidget(self.import_panel)
        elif item.text() == 'Statistics':
            print("stats btn clicked")
            statistics_window = StatisticsWindow()
            self.right_panel.addWidget(statistics_window)

    @property
    def home_logo(self):
        return self.__home_logo
    
    @property
    def stream_logo(self):
        return self.__stream_logo
    
    @property
    def list_widget_get(self):
        return self.list_widget


    def add_list_item_nav(self, text, icon_url):
        item = QListWidgetItem()
        item.setSizeHint(QSize(60, 60))  # Set the size of the item

        # Configure the button with the icon
        btn = QPushButton()
        btn.setStyleSheet("""
            QPushButton {
                min-height: 35px;
                border: none;
                background-color: transparent;
                color: black;
            }
            QPushButton:hover{
                background-color: transparent; 
                border: none;       
            }
        """)
        # btn.setStyleSheet("margin:-5px;")
        btn.setIcon(QIcon(icon_url))  # Use the provided icon URL
        btn.setIconSize(QSize(30, 30))  # Set the size of the icon
        btn.setText("")  # No text on the button, as we're using a label below

        # Configure the label for the text below the icon
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 10px; color: black; margin-top:7px;position:absolute;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create a container widget to hold the button (with icon) and the text label vertically
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(btn)
        container_layout.addWidget(text_label)

        # Set hover style for the container widget
        container.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QWidget:hover {
                background-color: #d0d0d0;  # Change to your desired hover background color
            }
        """)

        # Set the container widget as the item's widget
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)



