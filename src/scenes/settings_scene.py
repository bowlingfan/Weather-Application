from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from config import ConfigurationClass

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()
    
    def create_widgets(self):
        self.input_text_box = QLineEdit()
        self.confirm_button = QPushButton("Change Location")
        self.update_button = QPushButton("Update Weather Data")
        self.warning_label = QLabel("Updates Weather Data given current location; WILL freeze program.")
        self.error_label = QLabel("Test Error")

    def design_widgets(self):
        self.input_text_box.setFont(self.config.default_font)
        self.confirm_button.setFont(self.config.default_font)
        self.update_button.setFont(self.config.default_font)
        self.warning_label.setFont(self.config.default_font_small)
        self.error_label.setFont(self.config.default_font_small)
        self.error_label.setVisible(False)
        self.error_label.setStyleSheet("QLabel { color: #910700 }")

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(65,15,65,15)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.input_text_box)
        self.input_layout.addWidget(self.confirm_button)

        self.update_layout = QVBoxLayout()
        self.update_layout.addWidget(self.update_button)
        self.update_layout.addWidget(self.warning_label)
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.error_layout = QVBoxLayout()
        self.error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_layout.addWidget(self.error_label)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.update_layout)
        self.main_layout.addLayout(self.error_layout)


        self.setLayout(self.main_layout)

    def connect_events(self):
        pass

