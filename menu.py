from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Discord-like Navigation")

        # Create the main layout
        layout = QVBoxLayout()

        # Create the sidebar with buttons
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setLayout(QVBoxLayout())
        self.sidebar.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add buttons to the sidebar
        for i in range(5):
            btn = QPushButton()
            btn.setIcon(QIcon("img/home.svg"))  # Set the icon here
            btn.setIconSize(QSize(64, 64))  # Increase the size of the icon
            btn.setText("")  # Remove the text from the button

            label = QLabel(f"Button {i+1}")  # Create a label for the text
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create a layout for the button and label
            btn_layout = QVBoxLayout()
            btn_layout.addWidget(btn)
            btn_layout.addWidget(label)

            # Create a widget to hold the layout and add it to the sidebar
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            self.sidebar.layout().addWidget(btn_widget)

        # Add the sidebar and main area to the layout
        layout.addWidget(self.sidebar)

        # Set the window's main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
