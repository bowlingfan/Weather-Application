from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
)
class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        pass

    def design_widgets(self):
        pass

    def design_layouts(self):
        pass

    def connect_events(self):
        pass