from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
)
import configs.config as main_config
import configs.ui_config as ui_config

class SnapshotWidget(QWidget):
    def __init__(self, snapshotData):
        super().__init__()

        self.location_label = ui_config.UI_TextLabel(snapshotData["location"])
        self.date_label = ui_config.UI_TextLabel(snapshotData["date"])
        self.timestamp_label = ui_config.UI_TextLabel(snapshotData["timestamp"])
        self.temperature_label = ui_config.UI_TextLabel(str(snapshotData["temperature"]))
        self.delete_button = ui_config.UI_Button(ui_config.UI_History_Scene_Config["delete_button"]["default_txt"])

        self.date_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.timestamp_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        font = self.temperature_label.font()
        font.setPointSize(ui_config.UI_History_Scene_Config["temperature_label"]["font_size"])
        self.temperature_label.setFont(font)

        self.main_layout = QHBoxLayout()
        self.details_column = QVBoxLayout()

        self.details_column.addWidget(self.location_label)
        self.details_column.addWidget(self.date_label)
        self.details_column.addWidget(self.timestamp_label)
        self.details_column.addSpacing(3)
        self.details_column.addWidget(self.delete_button)

        self.main_layout.addLayout(self.details_column)
        self.main_layout.addWidget(self.temperature_label)
        self.setFixedWidth(200)
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

    def make_snapshots(self, database_data, records_amt):
        self.clear_scrolling_area_layout()

        widget_holder = QWidget()
        layout_holder = QHBoxLayout()
        layout_holder.setAlignment(Qt.AlignmentFlag.AlignLeft)
        current_col_index = 0
        for record in database_data:
            current_col_index += 1
            layout_holder.addWidget(SnapshotWidget(record))
            if current_col_index == 3:
                current_col_index = 0
                widget_holder.setLayout(layout_holder)
                self.add_to_scroll_area(widget_holder)
                widget_holder = QWidget()
                layout_holder = QHBoxLayout()
                layout_holder.setAlignment(Qt.AlignmentFlag.AlignLeft)
        widget_holder.setLayout(layout_holder)
        self.add_to_scroll_area(widget_holder)

        self.header.setText(f'{records_amt} / 30 snapshots.')