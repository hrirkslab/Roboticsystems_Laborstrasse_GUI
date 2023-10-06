import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QTabWidget, QTableWidget, QWidget, QTextEdit, QPushButton)
from PyQt6.QtGui import QPixmap, QIcon, QImageReader
from PyQt6.QtCore import Qt, QSize
from left_navigation import LeftNavigation
from statistics_window import StatisticsWindow

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.__stream_logo = "img/stream.svg"
        self.__home_logo = "img/home.svg"

    def init_ui(self):
        # Central widget and layout
        self.central_widget = QWidget(self)
        self.layout = QHBoxLayout(self.central_widget)
        

        url_to_logo = "img/home.svg"
        self.left_nav_ui()
        self.right_panel_ui()
        # Initialize Import and Statistics panels but do not add them to right_panel yet
        self.home_panel = self.left_nav.create_home_panel()
        self.import_panel = self.left_nav.create_import_panel()
        self.statistics_panel = self.left_nav.create_statistics_panel()

        self.right_panel.addWidget(self.home_panel)
        self.left_nav.list_widget.itemClicked.connect(self.on_item_clicked)

        self.setCentralWidget(self.central_widget)
        self.layout.addWidget(self.right_panel_widget)
        self.setWindowTitle('Dashboard')
        self.setGeometry(100, 100, 1200, 800)

        # Load styles from QSS
        with open("stylesheet/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.show()

    # Left Panel
    def left_nav_ui(self):
        self.left_nav = LeftNavigation()
        self.layout.addWidget(self.left_nav)
        self.left_nav.add_list_item_nav('Home', self.left_nav.home_logo)  
        self.left_nav.add_list_item_nav('Statistics', self.left_nav.home_logo)  
        self.left_nav.add_list_item_nav('Import', self.left_nav.home_logo) 
        


    # Right Panel
    def right_panel_ui(self):
        self.right_panel = QVBoxLayout()
        self.right_panel.setContentsMargins(0, 0, 0, 0)  # Remove margins from the right panel layout
        self.right_panel_widget = QWidget()
        self.right_panel_widget.setLayout(self.right_panel)
        
    def get_pixmap_from_url(self, url):
        image_reader = QImageReader(url)
        image = image_reader.read()
        return QPixmap.fromImage(image)

    
    
    def on_item_clicked(self, item):
        # Clear the right panel and add the corresponding widget based on clicked item
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

    def add_card(self, row):
        # Create a card-like widget
        card_widget = QWidget()
        card_layout = QHBoxLayout(card_widget)

        # Paths to image icons
        path_to_dna_icon = "img/dna.svg"
        path_to_circle_icon = "img/circle.svg"
        path_to_arrow_icon = "img/arrow-right.svg"

        # Create a DNA icon label (assuming it's common to all stations)
        dna_label = QLabel()
        dna_label.setPixmap(QPixmap(path_to_dna_icon))
        dna_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        for i in range(3):  # Example: 3 stations in each card
            station_widget = QWidget()
            station_layout = QVBoxLayout(station_widget)

            circle_label = QLabel()
            circle_label.setPixmap(QPixmap(path_to_circle_icon).scaledToWidth(30))  # Grey Circle representing station
            circle_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            # Add the DNA Icon only to the first station
            if i == 0:
                station_layout.addWidget(dna_label)

            station_layout.addWidget(circle_label)
            card_layout.addWidget(station_widget)

            if i < 2:  # Add an arrow between stations, except after the last station
                arrow_label = QLabel()
                arrow_label.setPixmap(QPixmap(path_to_arrow_icon).scaledToWidth(30))
                card_layout.addWidget(arrow_label)

        # Set the card widget as the cell widget in the table
        self.table_widget.setCellWidget(row, 0, card_widget)



def main():
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()