from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QLineEdit 
)
import configs.config as main_config
import configs.ui_config as ui_config

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        #self.connect_events()

    def create_widgets(self):
        self.header = ui_config.UI_TextLabel(ui_config.UI_Welcome_Scene_Config["header"]["default_txt"])
        self.guide = ui_config.UI_TextLabel(ui_config.UI_Welcome_Scene_Config["guide"]["default_txt"])
        self.location_text_box = QLineEdit()
        self.confirm_button = ui_config.UI_Button(ui_config.UI_Welcome_Scene_Config["confirm_button"]["default_txt"])

    def design_widgets(self):
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.guide.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.guide.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])

        self.location_text_box.setFixedSize(ui_config.UI_Welcome_Scene_Config["location_text_box"]["fixed_size"])
        self.location_text_box.setFont(ui_config.UI_Config["default"]["font"]["QFont_normal"])

        self.confirm_button.setFixedSize(ui_config.UI_Welcome_Scene_Config["confirm_button"]["fixed_size"])

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_interaction_layout = QHBoxLayout()
        self.user_interaction_layout.addWidget(self.location_text_box)
        self.user_interaction_layout.addWidget(self.confirm_button)
        
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.guide)
        self.main_layout.addLayout(self.user_interaction_layout)
        
        self.setLayout(self.main_layout)