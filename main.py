import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    messageSignal = pyqtSignal(str)

    def run(self):
        # Replace 'python' with 'python3' on Linux/Mac
        process = subprocess.Popen(["python", "child_process.py"],
                                   stdout=subprocess.PIPE,
                                   text=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.messageSignal.emit(output.strip())

        rc = process.poll()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.worker_thread = WorkerThread()
        self.worker_thread.messageSignal.connect(self.handle_message)

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.start_button = QPushButton('Start Child Process', self)
        self.start_button.clicked.connect(self.start_child_process)
        
        self.layout.addWidget(self.start_button)

    def start_child_process(self):
        self.worker_thread.start()

    def handle_message(self, message):
        print("Message from child process:", message)

def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
