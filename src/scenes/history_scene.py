from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QScrollArea,
    QPushButton
)
#from PyQt6.QtGui import QSiz
import configs.config as main_config
import configs.ui_config as ui_config
from data_read import history_data

class SnapshotWidget(QWidget):
    def __init__(self, snapshotData):
        super().__init__()

        self.location_label = ui_config.UI_TextLabel(ui_config.UI_History_Scene_Config["location_label"]["default_txt"])
        self.date_label = ui_config.UI_TextLabel(ui_config.UI_History_Scene_Config["date_label"]["default_txt"])
        self.timestamp_label = ui_config.UI_TextLabel(ui_config.UI_History_Scene_Config["timestamp_label"]["default_txt"])
        self.temperature_label = ui_config.UI_TextLabel(ui_config.UI_History_Scene_Config["temperature_label"]["default_txt"])
        self.delete_button = ui_config.UI_Button(ui_config.UI_History_Scene_Config["delete_button"]["default_txt"])

        self.date_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.timestamp_label.setFont(ui_config.UI_Config["default"]["font"]["QFont_small"])
        self.temperature_label.font().setPointSize(ui_config.UI_History_Scene_Config["temperature_label"]["font_size"])

        self.main_layout = QHBoxLayout()
        self.details_column = QVBoxLayout()

        self.details_column.addWidget(self.location_label)
        self.details_column.addWidget(self.date_label)
        self.details_column.addWidget(self.timestamp_label)
        self.details_column.addSpacing(3)
        self.details_column.addWidget(self.delete_button)

        self.main_layout.addLayout(self.details_column)
        self.main_layout.addWidget(self.temperature_label)

        #self.setMaximumSize(QSize(207, 153))
        self.setLayout(self.main_layout)

class Scene(ui_config.Base_Scene_ScrollArea):
    def __init__(self):
        super().__init__()

        self.historyDatabase = history_data.HistoryDatabase()
        
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()



        #print(self.scrolling_widget.size())

    def add_to_scroll_are(self, QUIObject):
        # OVERRIDE
        self.scrolling_area_layout.addLayout(QUIObject)
"""
        for i in range(10):
            widgets=QWidget()
            holder=QHBoxLayout()
            holder.addWidget(SnapshotWidget([]))
            holder.addWidget(SnapshotWidget([]))
            holder.addWidget(SnapshotWidget([]))
            widgets.setLayout(holder)
            self.scrolling_area_layout.addWidget(widgets)
"""