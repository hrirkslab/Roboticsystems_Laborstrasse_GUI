import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                            QTabWidget, QTableWidget, QWidget, QTextEdit, QPushButton)
from PyQt6.QtGui import QPixmap, QIcon, QImageReader
from PyQt6.QtCore import Qt, QSize
from statistics_window import StatisticsWindow

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the Central Widget and Layout
        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins from the main layout

        # Create Left Panel
        self.left_panel = QVBoxLayout()
        self.left_panel.setContentsMargins(0, 0, 0, 0)  # Remove margins from the left panel layout
        self.left_panel_widget = QWidget()
        self.left_panel_widget.setLayout(self.left_panel)
        self.left_panel_widget.setFixedWidth(80)
        self.left_panel_widget.setMinimumHeight(60)
        self.left_panel_widget.setStyleSheet("background-color: #eeeeee; color: #000000;border:none; min-height:25px")  

        url_to_logo = "img/home.svg"
        laboratory = "img/laboratory.svg"
        
        # Create Right Panel
        self.right_panel = QVBoxLayout()
        self.right_panel.setContentsMargins(0, 0, 0, 0)  # Remove margins from the right panel layout
        self.right_panel_widget = QWidget()
        self.right_panel_widget.setLayout(self.right_panel)
        self.right_panel_widget.setStyleSheet("background-color: #eeeeee; color: #000000;")  # Set font color to black and background to light gray

        # Load logo from the URL
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.get_pixmap_from_url(laboratory).scaledToWidth(60))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_panel.addWidget(self.logo_label)

        self.list_widget = QListWidget()
        self.list_widget.minimumHeight = 50
        # self.list_widget.setFixedWidth(100)
        self.add_list_item('Home', url_to_logo)
        self.add_list_item('Import', url_to_logo)
        self.add_list_item('Statistics', url_to_logo)
        layout = QVBoxLayout(self)
        self.left_panel.addWidget(self.list_widget)
        

        # Connect the itemClicked signal to the slot
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        
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
         # Load styles from QSS
        with open("stylesheet/styles.qss", "r") as f:
            self.setStyleSheet(f.read())



    def add_list_item(self, text, icon_url):
        item = QListWidgetItem()
        item.setSizeHint(QSize(60, 80))  # Set the size of the item

        # Configure the button with the icon
        btn = QPushButton()
        btn.setIcon(QIcon(icon_url))  # Use the provided icon URL
        btn.setIconSize(QSize(35, 35))  # Set the size of the icon
        btn.setText("")  # No text on the button, as we're using a label below
        btn.clicked.connect(lambda: self.on_item_clicked_new(text))

        # Configure the label for the text below the icon
        label = QLabel(text)
        label.setStyleSheet("font-size: 10px;")  # Make the text smaller
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a layout for the button and label
        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(label)

        # Create a widget to hold the layout and set it as the item's widget
        widget = QWidget()
        widget.setLayout(layout)
        
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def on_item_clicked_new(self, text):
        print(text+" clicked!")

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
        tab_widget.addTab(live_tab, QIcon(url_to_logo), 'Live')
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

        if item == 'Home':
            self.right_panel.addWidget(self.home_panel)
        elif item == 'Import':
            self.right_panel.addWidget(self.import_panel)
        elif item == 'Statistics':
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
