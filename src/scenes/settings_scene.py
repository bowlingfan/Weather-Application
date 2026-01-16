from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
import configs.config as main_config
import configs.ui_config as ui_config

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()
    
    def create_widgets(self):
        self.input_text_box = QLineEdit()
        self.confirm_button = QPushButton(ui_config.UI_Settings_Scene_Config["confirm_button"]["default_txt"])
        self.update_button = QPushButton(ui_config.UI_Settings_Scene_Config["update_button"]["default_txt"])
        self.warning_label = QLabel(ui_config.UI_Settings_Scene_Config["warning_label"]["default_txt"])
        self.error_label = QLabel(ui_config.UI_Settings_Scene_Config["error_label"]["default_txt"])

    def design_widgets(self):
        self.input_text_box.setFont(ui_config.UI_Config["default"]["font"]["QFont_normal"])
        self.confirm_button.setFont(ui_config.UI_Config["default"]["font"]["QFont_normal"])
        self.update_button.setFont(ui_config.UI_Config["default"]["font"]["QFont_normal"])
        self.warning_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.error_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])

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

