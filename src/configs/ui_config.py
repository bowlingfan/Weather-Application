from PyQt6.QtCore import Qt, QSize, QMargins
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout
)
from PyQt6.QtGui import QFont, QFontDatabase
"""
PRIVATE VARIABLES IF NOT IN class.__init__()
"""
default_font_directory = "resource/Roboto-Light.ttf"

UI_Config = {
    "default": {
        "font": {
            "size": {
                "small": 9,
                "normal": 15,
            },
            "QFont_normal": None,
            "QFont_small": None,
        },
    },
    "window": {
        "width": 700,
        "height": 350,
        "title": "Weather Application",
    },
}

# Ex. Menu Buttons
UI_Non_Scene_Config = {
    "menu_button": {
        "default_txt": "MENU",
        "maximum_size": QSize(35,35),
        "minimum_size": QSize(0, 35),
        "holder_maximum_size": QSize(50, 50),
        "widget_holder_maximum_width": 125,
        # todo "Icon"
    },

    "menu_layout": {
        "holder_layout_margins": QMargins(15,15,0,0),
        "holder_layout_spacing": 0,
        "widget_layout_margins": QMargins(15,0,0,0),
        "widget_layout_spacing": 0,
    },

    "home_button": {
        "default_txt": "Home",
    },

    "warnings_button": {
        "default_txt": "Warnings",
    },

    "details_button": {
        "default_txt": "Details",
    },

    "settings_button": {
        "default_txt": "Settings",
    },

    "history_button": {
        "default_txt": "History",
    },

    "day_display_row": {
        "spacing": 10
    }
}

UI_Welcome_Scene_Config = {
    "header": {
        "default_txt": "Hi!",
    },

    "guide": {
        "default_txt": "Type a location in the United States and press confirm to get started."
    },

    "location_text_box": {
        "fixed_size": QSize(290,35)
    },

    "confirm_button": {
        "default_txt": "CONFIRM",
        "fixed_size": QSize(110,35)
    },
}

UI_Home_Scene_Config = {
    "general": {
        "QLabel_Max_Height": 15
    },

    "location_header": {
        "default_txt": "LOCATION HEADER",
        "minimum_height": 45
    },

    "temperature_display": {
        "default_txt": "TEMP",
        "maximum_height": UI_Config["window"]["height"],
        "font_size": 80,
    },

    "forecast_display": {
        "default_txt": "FORECAST",
    },

    "preciptation_display": {
        "default_txt": "PRECIPITATION",
    },

    "wind_display": {
        "default_txt": "WIND",
    },

    "message": {
        "default_txt": "MESSAGE DEMO",
    },
}

UI_Details_Scene_Config = {
    "decrement_day_button": {
        "default_txt": "<",
        "fixed_size": QSize(35, 35),
    },

    "increment_day_button": {
        "default_txt": ">",
        "fixed_size": QSize(35, 35),
    },

    "DetailsLabel": {
        "maximum_height": 15
    },

    "day_display": {
        "default_txt": "DayName - Month Day",
        "maximum_height": 35,
    },

    "temperature_high_display": {
        "default_txt": "High Temperature 100°",
    },

    "temperature_low_display": {
        "default_txt": "Low Temperature -10°",
    },

    "precipitation_chance_display": {
        "default_txt": "PRECIPITATION",
    },

    "wind_display": {
        "default_txt": "WIND",
    },

    "forecasted_weather_display": {
        "default_txt": "FORECAST",
        "maximum_height": 35,
    },

    "precipitation_bar": {
        "fixed_height": 200,
    }
}

UI_Settings_Scene_Config = {
    "confirm_button": {
        "default_txt": "Change Location"
    },

    "update_button": {
        "default_txt": "Update Weather Data"
    },

    "warning_label": {
        "default_txt": "Updates Weather Data given current location; WILL freeze program."
    },

    "error_label": {
        "default_txt": "Test Error"
    },
}

UI_Warnings_Scene_Config = {
    "status_label": {
        "default_txt": "WARNING"
    },

    "message_label": {
        "default_txt": "..."
    }, 
}

UI_History_Scene_Config = {
    "location_label": {
        "default_txt": "location"
    },

    "date_label": {
        "default_txt": "date"
    },

    "timestamp_label": {
        "default_txt": "timestamp"
    },

    "temperature_label": {
        "default_txt": "temperature",
        "font_size": 45,
    },

    "header_snapshot_amount": {
        "default_txt": "0 / 30 snapshots.",
        "fixed_height": 35,
    },

    "delete_button": {
        "default_txt": "DELETE",
    }
}

UI_Base_Scene_ScrollArea_Config = {
    "header_fixed_height": 35,
    "header_default_txt": "HEADER",
    "scrolling_widget_empty_indicator_default_txt": "SCROLLING AREA EMPTY"
}

"""
If any specific changes must be made,
You should use properties first.

Only use inheritance when it will be used for more than one object.
"""
class UI_Button(QPushButton):
    def __init__(self, text):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(UI_Config["default"]["font"]["QFont_normal"])

class UI_TextLabel(QLabel):
    def __init__(self, text):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(UI_Config["default"]["font"]["QFont_normal"])
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class Base_Scene_ScrollArea(QWidget):
    def __init__(self):
        super().__init__()

        self.list_of_widgets_displayed = []
    
    def create_widgets(self):
        self.header = UI_TextLabel(UI_Base_Scene_ScrollArea_Config["header_default_txt"])#, .default_font)
        self.scrolling_widget_empty_indicator = UI_TextLabel(UI_Base_Scene_ScrollArea_Config["scrolling_widget_empty_indicator_default_txt"]) #random.choice(.warnings_config.no_weather_warning_messages), .default_font)
        self.scrolling_widget = QWidget()
        self.scrolling_area = QScrollArea()

    def design_widgets(self):
        self.header.setFixedHeight(UI_Base_Scene_ScrollArea_Config["header_fixed_height"])
        self.header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.scrolling_widget_empty_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrolling_widget_empty_indicator.setVisible(False)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15,15,15,15)

        self.scrolling_area_layout = QVBoxLayout()
        self.scrolling_area_layout.setContentsMargins(0,0,0,0)
        self.scrolling_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrolling_widget.setLayout(self.scrolling_area_layout)

        self.scrolling_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrolling_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrolling_area.setWidgetResizable(True)
        self.scrolling_area.setWidget(self.scrolling_widget)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.scrolling_widget_empty_indicator)
        self.main_layout.addWidget(self.scrolling_area)

        self.setLayout(self.main_layout)

    def clear_scrolling_area_layout(self):
        for widget in self.list_of_widgets_displayed:
            widget.deleteLater()
        self.list_of_widgets_displayed.clear()

    def update_amount_to_scene(self, amt, strtype):
        if amt <= 0:
            self.scrolling_widget.setVisible(False)
            self.scrolling_widget_empty_indicator.setVisible(True)
        else:
            self.header.setText(f"{amt} {strtype}s.")
            self.scrolling_widget_empty_indicator.setVisible(False)
            self.scrolling_widget.setVisible(True)

    def add_to_scroll_area(self, QUIObject):
        # WARNING: THIS IS ONLY TO DISPLAY THE BASE CODE. MUST OVERRIDE.
        raise BaseException("MUST BE OVERRIDEN. THIS IS THE BASE CODE.")
    
        self.scrolling_area_layout.addWidget(QUIObject)
        self.scrolling_area_layout.addLayout(QUIObject)

    def connect_events(self):
        pass

"""
DECLARE IN MAIN.PY.
"""
def make_font():
    qid = QFontDatabase.addApplicationFont(default_font_directory)
    # There is only 1 child font of the given Font Family.
    UI_Config["default"]["font"]["QFont_normal"] = QFont(QFontDatabase.applicationFontFamilies(qid)[0])
    UI_Config["default"]["font"]["QFont_normal"].setPointSize(UI_Config["default"]["font"]["size"]["normal"])
    UI_Config["default"]["font"]["QFont_small"] = QFont(QFontDatabase.applicationFontFamilies(qid)[0])
    UI_Config["default"]["font"]["QFont_small"].setPointSize(UI_Config["default"]["font"]["size"]["small"])