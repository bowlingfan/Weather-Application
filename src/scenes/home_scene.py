from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
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
        self.location_header = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["location_header"]["default_txt"])
        self.temperature_display = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["temperature_display"]["default_txt"])
        # detailed
        self.forecast_display = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["forecast_display"]["default_txt"])
        self.preciptation_display = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["preciptation_display"]["default_txt"])
        self.wind_display = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["wind_display"]["default_txt"])
        self.message = ui_config.UI_TextLabel(ui_config.UI_Home_Scene_Config["message"]["default_txt"])

    def design_widgets(self):
        self.location_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.location_header.setMinimumHeight(ui_config.UI_Home_Scene_Config["location_header"]["minimum_height"])

        self.temperature_display.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
        self.temperature_display.setMaximumHeight(ui_config.UI_Config["window"]["height"])
        new_font = self.temperature_display.font()
        new_font.setPointSize(ui_config.UI_Home_Scene_Config["temperature_display"]["font_size"])
        self.temperature_display.setFont(new_font)

        self.forecast_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.forecast_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.preciptation_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.preciptation_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.wind_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.wind_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.message.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()

        self.header_row = QHBoxLayout()
        self.header_row.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.main_info_row = QHBoxLayout()
        self.main_info_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detailed_info = QVBoxLayout()
        self.detailed_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_row = QHBoxLayout()
        self.msg_row.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.header_row.addWidget(self.location_header)
        self.main_info_row.addWidget(self.temperature_display)
        self.main_info_row.addLayout(self.detailed_info)
        self.detailed_info.addWidget(self.forecast_display)
        self.detailed_info.addWidget(self.preciptation_display)
        self.detailed_info.addWidget(self.wind_display)
        self.msg_row.addWidget(self.message)

        self.main_layout.addLayout(self.header_row)
        self.main_layout.addLayout(self.main_info_row)
        self.main_layout.addLayout(self.msg_row)

        self.setLayout(self.main_layout)
    
    def connect_events(self):
        pass