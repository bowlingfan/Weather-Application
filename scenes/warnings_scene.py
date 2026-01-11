from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QScrollArea
)
from config import ConfigurationClass
import random

severity_to_color = {
    1:"QLabel {background-color: #A5000D; color: #FFFFFF}",
    2:"QLabel {background-color: #FF8800; color: #FFFFFF}",
}

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)

class WarningWidget(QWidget):
    def __init__(self, severityID, config : ConfigurationClass):
        super().__init__()
        self.config = config
        self.main_layout = QVBoxLayout()

        self.status_label = TextLabel("WARNING", config.default_font)
        self.status_label.setStyleSheet(severity_to_color[severityID])
        self.status_label.setContentsMargins(5,5,5,5)
        self.message_label = TextLabel("...",config.make_font(config.default_font_small_size+2))
        self.message_label.setWordWrap(True)
        
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.message_label)

        self.setLayout(self.main_layout)

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        self.header_alert_amount = TextLabel("3 weather alerts.", self.config.default_font)
        self.no_weather_warnings = TextLabel(random.choice(self.config.warnings_config.no_weather_warning_messages), self.config.default_font)
        self.scrolling_widget = QWidget()
        self.scrolling_area_warnings = QScrollArea()

    def design_widgets(self):
        self.header_alert_amount.setMaximumHeight(35)
        self.header_alert_amount.setMinimumHeight(35)
        self.header_alert_amount.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.no_weather_warnings.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_weather_warnings.setVisible(False)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15,15,15,15)

        self.scrolling_area_layout = QVBoxLayout()
        self.scrolling_area_layout.setContentsMargins(0,0,0,0)
        self.scrolling_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrolling_widget.setLayout(self.scrolling_area_layout)

        self.scrolling_area_warnings.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrolling_area_warnings.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrolling_area_warnings.setWidgetResizable(True)
        self.scrolling_area_warnings.setWidget(self.scrolling_widget)

        self.main_layout.addWidget(self.header_alert_amount)
        self.main_layout.addWidget(self.no_weather_warnings)
        self.main_layout.addWidget(self.scrolling_area_warnings)

        self.setLayout(self.main_layout)

    def connect_events(self):
        pass

    def make_alerts(self, alert_data, geocode_data):
        for x in range(len(self.scrolling_area_layout.children())):
            self.scrolling_area_layout.takeAt(0)
        alerts = alert_data.alerts
        alerts_amt = len(alerts)
        if alerts_amt == 0:
            self.scrolling_area_warnings.setVisible(False)
            self.no_weather_warnings.setVisible(True)
        else:
            self.scrolling_area_warnings.setVisible(True)
            self.no_weather_warnings.setVisible(False)
            for alert in alerts:
                warningWidget = WarningWidget(alert.severity, self.config)
                warningWidget.status_label.setText(alert.event_name)
                warningWidget.message_label.setText(f"Expires Approximately: {alert.get_expire_time_in_datetime()}\n\n{alert.description}")
                self.scrolling_area_layout.addWidget(warningWidget)
        self.header_alert_amount.setText(f"{alerts_amt} weather alerts in {geocode_data.get_location()}.")