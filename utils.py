from PyQt6.QtGui import QPixmap, QImageReader
from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QListWidgetItem, QWidget, QPushButton)
from PyQt6.QtGui import QPixmap, QIcon, QImageReader
from PyQt6.QtCore import Qt, QSize

class Utils:
    @staticmethod
    def get_pixmap_from_url(url):
        image_reader = QImageReader(url)
        image = image_reader.read()
        return QPixmap.fromImage(image)
    