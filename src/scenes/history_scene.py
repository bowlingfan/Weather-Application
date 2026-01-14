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
from config import ConfigurationClass
from data_read import history_data

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)

class SnapshotWidget(QWidget):
    def __init__(self, config : ConfigurationClass, snapshotData):
        super().__init__()

        self.location_label = TextLabel("location", config.default_font)
        self.date_label = TextLabel("date", config.default_font_small)
        self.timestamp_label = TextLabel("timestamp", config.default_font_small)
        self.temperature_label = TextLabel("105°", config.make_font(30))
        self.delete_button = QPushButton("DELETE")

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

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.historyDatabase = history_data.HistoryDatabase()
        
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

        print(self.scrolling_widget.size())

    def create_widgets(self):
        self.header_snapshot_amount = TextLabel("0 / 30 snapshots.", self.config.default_font)
        #self.no_snapshots_display = TextLabel(random.choice(self.config.warnings_config.no_weather_warning_messages), self.config.default_font)
        self.scrolling_widget = QWidget()
        self.scrolling_area_snapshots = QScrollArea()
        
    def design_widgets(self):
        self.header_snapshot_amount.setMaximumHeight(35)
        self.header_snapshot_amount.setMinimumHeight(35)
        self.header_snapshot_amount.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        #self.no_snapshots_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.no_snapshots_display.setVisible(False)
    
    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15,15,15,15)

        self.scrolling_area_layout = QVBoxLayout()
        self.scrolling_area_layout.setContentsMargins(0,0,0,0)
        self.scrolling_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrolling_widget.setLayout(self.scrolling_area_layout)

        self.scrolling_area_snapshots.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrolling_area_snapshots.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrolling_area_snapshots.setWidgetResizable(True)
        self.scrolling_area_snapshots.setWidget(self.scrolling_widget)

        self.main_layout.addWidget(self.header_snapshot_amount)
        #self.main_layout.addWidget(self.no_weather_warnings)
        self.main_layout.addWidget(self.scrolling_area_snapshots)

        self.setLayout(self.main_layout)

    def connect_events(self):
        for i in range(10):
            widgets=QWidget()
            holder=QHBoxLayout()
            holder.addWidget(SnapshotWidget(self.config, []))
            holder.addWidget(SnapshotWidget(self.config, []))
            holder.addWidget(SnapshotWidget(self.config, []))
            widgets.setLayout(holder)
            self.scrolling_area_layout.addWidget(widgets)