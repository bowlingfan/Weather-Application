from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QStackedLayout,
)
from config import ConfigurationClass

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)
        self.setMaximumHeight(15)

class UIButton(QPushButton):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        self.menu_button = UIButton("MENU", self.config.default_font)
        self.location_header = TextLabel("Location Test", self.config.default_font)
        self.temperature_display = TextLabel("75°",self.config.make_font(80))
        # detailed
        self.feels_like_display = TextLabel("Feels like: ", self.config.default_font_small)
        self.preciptation_display = TextLabel("Preciptation: ", self.config.default_font_small)
        self.wind_display = TextLabel("Wind: 6 N", self.config.default_font_small)
        self.message = TextLabel("Aren't you excited? It's sunny.", self.config.default_font_small)

        self.home_button = UIButton("Home", self.config.default_font_small)
        self.warnings_button = UIButton("Warnings", self.config.default_font_small)
        self.detailed_button = UIButton("Detailed", self.config.default_font_small)

    def design_widgets(self):
        self.menu_button.setMaximumSize(35,35)

        self.location_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.location_header.setFont(self.config.default_font)

        self.temperature_display.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
        self.temperature_display.setMaximumHeight(300)

        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def design_layouts(self):
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.menu_widget = QWidget()
        self.menu_main_layout = QVBoxLayout()

        self.container_widget = QWidget()
        self.container_main_layout = QVBoxLayout()
        """
        menu_widget setup
        """
        self.menu_main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        self.menu_widget.setMaximumWidth(150)

        self.menu_main_layout.addWidget(self.home_button)
        self.menu_main_layout.addWidget(self.warnings_button)
        self.menu_main_layout.addWidget(self.detailed_button)

        self.menu_widget.setLayout(self.menu_main_layout)
        self.menu_widget.setVisible(False)
        """
        container_page setup
        """
        self.container_main_layout.setSpacing(15)
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
        self.detailed_info.addWidget(self.feels_like_display)
        self.detailed_info.addWidget(self.preciptation_display)
        self.detailed_info.addWidget(self.wind_display)
        self.msg_row.addWidget(self.message)

        self.container_main_layout.addLayout(self.header_row)
        self.container_main_layout.addLayout(self.main_info_row)
        self.container_main_layout.addLayout(self.msg_row)

        self.container_widget.setLayout(self.container_main_layout)

        """
        finalize by adding widgets to main layout
        """
        self.main_layout.addWidget(self.container_widget)
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.menu_button)

        self.setLayout(self.main_layout)
    
    def connect_events(self):
        self.menu_button.clicked.connect(self.menu_button_clicked)

    def menu_button_clicked(self):
        self.menu_widget.setVisible(not self.menu_widget.isVisible())