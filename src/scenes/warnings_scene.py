from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
import configs.config as main_config
import configs.ui_config as ui_config

severity_to_color = {
    1:"QLabel {background-color: #A5000D; color: #FFFFFF}",
    2:"QLabel {background-color: #FF8800; color: #FFFFFF}",
    3:"QLabel {background-color: #2D0000; color: #FFFFFF}"
}


class WarningWidget(QWidget):
    def __init__(self, alert_data):
        super().__init__()
        self.main_layout = QVBoxLayout()

        severityID = alert_data.severity 
        event_name = alert_data.event_name
        expire_time = alert_data.get_expire_time_in_datetime()
        description = alert_data.description

        self.status_label = ui_config.UI_TextLabel(event_name)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setStyleSheet(severity_to_color[severityID])
        self.status_label.setContentsMargins(5,5,5,5)
        self.message_label = ui_config.UI_TextLabel(f"Expires Approximately: {expire_time}\n\n{description}")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.message_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.message_label.setWordWrap(True)
        
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.message_label)

        self.setLayout(self.main_layout)

class Scene(ui_config.Base_Scene_ScrollArea):
    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def add_to_scroll_area(self, QUIObject):
        self.scrolling_area_layout.addWidget(QUIObject)
        self.list_of_widgets_displayed.append(QUIObject)

    def make_alerts(self, alert_data, geocode_data):
        # clear all items
        self.clear_scrolling_area_layout()

        alerts = alert_data.alerts
        alerts_amt = len(alerts)
        if alerts_amt == 0:
            self.scrolling_area.setVisible(False)
            self.scrolling_widget_empty_indicator.setVisible(True)
            self.scrolling_widget_empty_indicator.setText(main_config.get_message_from_no_warnings())
        else:
            self.scrolling_area.setVisible(True)
            self.scrolling_widget_empty_indicator.setVisible(False)
            for alert in alerts:
                self.add_to_scroll_area(WarningWidget(alert))
        self.header.setText(f"{alerts_amt} weather alerts in {geocode_data.get_location()}.")