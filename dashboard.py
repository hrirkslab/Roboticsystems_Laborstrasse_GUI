import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                            QTabWidget, QTableWidget, QWidget, QTextEdit, QPushButton)
from PyQt6.QtGui import QPixmap, QIcon, QImageReader
from PyQt6.QtCore import Qt, QSize
from statistics_window import StatisticsWindow

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__stream_logo = "img/stream.svg"
        self.__home_logo = "img/home.svg"

        # Initialize the Central Widget and Layout
        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins from the main layout
        

        # Create Left Panel
        self.left_panel = QVBoxLayout()
        self.left_panel.setContentsMargins(0, 0, 0, 0)  # Remove margins from the left panel layout
        self.left_panel_widget = QWidget()
        self.left_panel_widget.setLayout(self.left_panel)
        self.left_panel_widget.setFixedWidth(60)
        self.left_panel_widget.setStyleSheet("min-height:75px;max-width:60px;padding-top:10px;")  

        url_to_logo = "img/home.svg"
        laboratory_logo = "img/laboratory.svg"
        
        

        # Load logo from the URL
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.get_pixmap_from_url(laboratory_logo).scaledToWidth(50))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        self.logo_label.setStyleSheet("margin-left:10px;margin-top:10px;")
        self.left_panel.addWidget(self.logo_label)

        self.list_widget = QListWidget()
        self.list_widget.minimumHeight = 50
        # self.list_widget.setIconSize(QSize(50, 50))
        self.add_list_item_nav('Home', self.__home_logo)
        self.add_list_item_nav('Import', url_to_logo)
        self.add_list_item_nav('Statistics', url_to_logo)
        # self.list_widget.setStyleSheet("background:#FF0000;")
        self.left_panel.addWidget(self.list_widget)
        

        # Connect the itemClicked signal to the slot
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        # Create Right Panel
        self.right_panel = QVBoxLayout()
        self.right_panel.setContentsMargins(0, 0, 0, 0)  # Remove margins from the right panel layout
        self.right_panel_widget = QWidget()
        self.right_panel_widget.setLayout(self.right_panel)
        self.right_panel_widget.setStyleSheet("background-color: #eeeeee; color: #000000;")  # Set font color to black and background to light gray

        # Home Panel
        self.home_panel = self.create_home_panel(url_to_logo)
        self.right_panel.addWidget(self.home_panel)

        # Initialize Import and Statistics panels but do not add them to right_panel yet
        self.import_panel = self.create_import_panel()
        self.statistics_panel = self.create_statistics_panel()

        self.layout.addWidget(self.left_panel_widget)
        self.layout.addWidget(self.right_panel_widget)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Dashboard')
        self.setGeometry(100, 100, 1200, 800)

    def add_list_item(self, text, icon_url):
        item = QListWidgetItem(QIcon(QPixmap(self.get_pixmap_from_url(icon_url))), text)
        self.list_widget.addItem(item)

    def add_list_item_nav(self, text, icon_url):
        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 50))  # Set the size of the item

        btn = QPushButton()
        btn.setStyleSheet("min-height:35px; hover:none; border:none;")
        btn.setIcon(QIcon("img/home.svg"))  # Set the icon here
        btn.setIconSize(QSize(30, 30))  # Increase the size of the icon
        btn.setText("")  # Remove the text from the button

        # icon = QIcon()
        # pixmap = QPixmap(self.get_pixmap_from_url(icon_url))
        # scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        # icon.addPixmap(scaled_pixmap)

        # Create a label for the text below the icon
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size:10px;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create a container widget to hold the icon and text label vertically
        container = QWidget()
        container_layout = QVBoxLayout(container)
        # container_layout.addWidget(icon_label)  # Add the icon label
        container_layout.addWidget(btn)  # Add the icon label
        container_layout.addWidget(text_label)  # Add the text label

        # Set the container widget as the item's widget
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)


    def get_pixmap_from_url(self, url):
        image_reader = QImageReader(url)
        image = image_reader.read()
        return QPixmap.fromImage(image)

    def create_home_panel(self, url_to_logo):
        home_panel = QWidget()
        home_layout = QVBoxLayout(home_panel)

        tab_widget = QTabWidget()
        live_tab = QWidget()
        live_tab_layout = QVBoxLayout(live_tab)
        table_widget = QTableWidget()
        table_widget.setColumnCount(6)
        table_widget.setHorizontalHeaderLabels(['Probe ID', 'Start Station', 'Übergang Station', 'Ende Station', 'Datum', 'Zeitdauer'])
        table_widget.setRowCount(5)
        live_tab_layout.addWidget(table_widget)
        tab_widget.addTab(live_tab, QIcon(self.__stream_logo), 'Live')
        tab_widget.addTab(QWidget(), QIcon(url_to_logo), 'Historical Data')

        home_layout.addWidget(tab_widget)
        return home_panel

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
        # Clear the right panel and add the corresponding widget based on clicked item
        for i in reversed(range(self.right_panel.count())): 
            self.right_panel.itemAt(i).widget().setParent(None)

        if item.text() == 'Home':
            self.right_panel.addWidget(self.home_panel)
        elif item.text() == 'Import':
            self.right_panel.addWidget(self.import_panel)
        elif item.text() == 'Statistics':
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
