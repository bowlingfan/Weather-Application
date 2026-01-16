from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QStackedLayout, 
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
)
import configs.config as main_config
import configs.ui_config as ui_config

class DetailsLabel(ui_config.UI_TextLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setMaximumHeight(ui_config.UI_Details_Scene_Config["DetailsLabel"]["maximum_height"])
        self.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        self.decrement_day_button = ui_config.UI_Button(ui_config.UI_Details_Scene_Config["decrement_day_button"]["default_txt"])
        self.increment_day_button = ui_config.UI_Button(ui_config.UI_Details_Scene_Config["increment_day_button"]["default_txt"])
        self.day_display = ui_config.UI_TextLabel(ui_config.UI_Details_Scene_Config["day_display"]["default_txt"])

        self.temperature_high_display = DetailsLabel(ui_config.UI_Details_Scene_Config["temperature_high_display"]["default_txt"])
        self.temperature_low_display = DetailsLabel(ui_config.UI_Details_Scene_Config["temperature_low_display"]["default_txt"])
        self.precipitation_chance_display = DetailsLabel(ui_config.UI_Details_Scene_Config["precipitation_chance_display"]["default_txt"])
        self.wind_display = DetailsLabel(ui_config.UI_Details_Scene_Config["wind_display"]["default_txt"])
        self.forecasted_weather_display = ui_config.UI_TextLabel(ui_config.UI_Details_Scene_Config["forecasted_weather_display"]["default_txt"])

        self.precipitation_bar = QWidget()

    def design_widgets(self):
        self.temperature_high_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.temperature_low_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.precipitation_chance_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.wind_display.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])

        self.precipitation_bar.setFixedHeight(ui_config.UI_Details_Scene_Config["precipitation_bar"]["fixed_height"])
        self.precipitation_bar.setStyleSheet("""
            QWidget {
                background-color: #0083FF
            }
        """)
        self.decrement_day_button.setFixedSize(ui_config.UI_Details_Scene_Config["decrement_day_button"]["fixed_size"])
        self.increment_day_button.setFixedSize(ui_config.UI_Details_Scene_Config["increment_day_button"]["fixed_size"])
        self.day_display.setMaximumHeight(ui_config.UI_Details_Scene_Config["day_display"]["maximum_height"])
        self.forecasted_weather_display.setMaximumHeight(ui_config.UI_Details_Scene_Config["forecasted_weather_display"]["maximum_height"])

    def design_layouts(self):
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        # Only used to add to QStackedLayout. Should not be used anywhere else.
        container_widget = QWidget()
        self.container_layout = QVBoxLayout()

        # Only used to add to QStackedLayout. Should not be used anywhere else.
        precipitation_bar_holder = QWidget()
        precipitation_bar_holder_layout = QVBoxLayout()

        precipitation_bar_holder_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        precipitation_bar_holder_layout.setContentsMargins(0,0,0,0)
        precipitation_bar_holder_layout.addWidget(self.precipitation_bar)

        self.day_display_row = QHBoxLayout()
        self.detailed_info_layout = QVBoxLayout()

        self.day_display_row.addWidget(self.decrement_day_button, 0, Qt.AlignmentFlag.AlignRight)
        self.day_display_row.addSpacing(ui_config.UI_Non_Scene_Config["day_display_row"]["spacing"])
        self.day_display_row.addWidget(self.day_display)
        self.day_display_row.addSpacing(ui_config.UI_Non_Scene_Config["day_display_row"]["spacing"])
        self.day_display_row.addWidget(self.increment_day_button, 0, Qt.AlignmentFlag.AlignLeft)

        self.detailed_info_layout.addWidget(self.temperature_high_display)
        self.detailed_info_layout.addWidget(self.temperature_low_display)
        self.detailed_info_layout.addWidget(self.precipitation_chance_display)
        self.detailed_info_layout.addWidget(self.wind_display)
        self.detailed_info_layout.addWidget(self.forecasted_weather_display)

        self.container_layout.setContentsMargins(65,15,65,15)
        self.container_layout.addLayout(self.day_display_row,2)
        self.container_layout.addLayout(self.detailed_info_layout)
        """
        final changes
        """
        container_widget.setLayout(self.container_layout)
        precipitation_bar_holder.setLayout(precipitation_bar_holder_layout)

        self.main_layout.addWidget(precipitation_bar_holder)
        self.main_layout.addWidget(container_widget)

        self.setLayout(self.main_layout)

    def connect_events(self):
        pass