from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QStackedWidget,
    QStackedLayout,
    QPushButton
)
from scenes import (
    details_scene,
    welcome_scene,
    home_scene,
    warnings_scene,
    settings_scene,
)
from config import ConfigurationClass
import datetime
#import inspect
#import os

class UIButton(QPushButton):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)
        
class MainApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.setFixedSize(self.config.window_width,self.config.window_width//2)
        self.setWindowTitle("Weather Application")

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()
    """
    Creating/Setup QT Window
    """
    def create_widgets(self):
        self.menu_widget = QWidget()
        self.menu_button_holder_widget = QWidget()
        self.menu_button = UIButton("MENU", self.config.default_font)

        self.home_button = UIButton("Home", self.config.default_font_small)
        self.warnings_button = UIButton("Warnings", self.config.default_font_small)
        self.details_button = UIButton("Details", self.config.default_font_small)
        self.settings_button = UIButton("Settings", self.config.default_font_small)
        self.history_button = UIButton("History", self.config.default_font_small)

        self.scenes = QStackedWidget()
        self.welcome_scene = welcome_scene.Scene()
        self.home_scene = home_scene.Scene()
        self.warnings_scene = warnings_scene.Scene()
        self.details_scene = details_scene.Scene()
        self.settings_scene = settings_scene.Scene()

    def design_widgets(self):
        self.menu_button.setMaximumSize(35,35)
        self.menu_button.setMinimumSize(0,35)
        self.menu_button_holder_widget.setMaximumSize(50,50)
        self.menu_widget.setVisible(False)
        self.menu_button.setVisible(False)
        self.menu_widget.setMaximumWidth(100)

    def design_layouts(self):
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll) 

        """
        scenes setup
        """
        self.scenes.addWidget(self.welcome_scene)
        self.scenes.addWidget(self.home_scene)
        self.scenes.addWidget(self.warnings_scene)
        self.scenes.addWidget(self.details_scene)
        self.scenes.addWidget(self.settings_scene)
        self.scenes.setCurrentIndex(self.config.scenes_available["welcome_scene"])
        """
        menu widget/button setup.

        local variables: menu_button_holder_layout & menu_widget_layout
        since they SHOULDN'T BE used other than to organize QT widgets.
        """
        menu_button_holder_layout = QVBoxLayout()
        menu_button_holder_layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        menu_button_holder_layout.setContentsMargins(15,15,0,0)
        menu_button_holder_layout.setSpacing(0)
        menu_button_holder_layout.addWidget(self.menu_button)
        self.menu_button_holder_widget.setLayout(menu_button_holder_layout)

        menu_widget_layout = QVBoxLayout()
        menu_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignLeft)
        menu_widget_layout.setContentsMargins(15,0,0,0)
        menu_widget_layout.setSpacing(5)
        menu_widget_layout.addWidget(self.home_button)
        menu_widget_layout.addWidget(self.warnings_button)
        menu_widget_layout.addWidget(self.details_button)
        menu_widget_layout.addWidget(self.settings_button)
        menu_widget_layout.addWidget(self.history_button)
        self.menu_widget.setLayout(menu_widget_layout)

        """
        main page setup
        """
        self.main_layout.addWidget(self.scenes)
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.menu_button_holder_widget)

        self.setLayout(self.main_layout)

    def connect_events(self):
        self.welcome_scene.confirm_button.clicked.connect(self.welcome_confirm_button_clicked)
        self.menu_button.clicked.connect(self.menu_button_clicked)
        self.home_button.clicked.connect(self.home_button_clicked)
        self.warnings_button.clicked.connect(self.warnings_button_clicked)
        self.details_button.clicked.connect(self.details_button_clicked)
        self.settings_button.clicked.connect(self.settings_button_clicked)
        self.settings_scene.confirm_button.clicked.connect(self.settings_change_location_button_clicked)
        self.settings_scene.update_button.clicked.connect(self.settings_update_location_button_clicked)
        self.details_scene.increment_day_button.clicked.connect(self.increment_button_clicked)
        self.details_scene.decrement_day_button.clicked.connect(self.decrement_button_clicked)

    def menu_button_clicked(self):
        self.menu_widget.setVisible(not self.menu_widget.isVisible())
    def home_button_clicked(self):
        self.menu_widget.setVisible(False)
        self.request_change_scene("home_scene")
    def warnings_button_clicked(self):
        self.menu_widget.setVisible(False)
        self.request_change_scene("warnings_scene")
    def details_button_clicked(self):
        self.menu_widget.setVisible(False)
        self.request_change_scene("details_scene")
    def settings_button_clicked(self):
        self.menu_widget.setVisible(False)
        self.settings_scene.error_label.setVisible(False)
        self.request_change_scene("settings_scene")
    def increment_button_clicked(self):
        self.config.weather_forecast_data.index_read += 1
        if self.config.weather_forecast_data.index_read >= len(self.config.weather_forecast_data.periods):
            self.config.weather_forecast_data.index_read = 0
        self.update_UI_weather_forecast_data()
    def decrement_button_clicked(self):
        self.config.weather_forecast_data.index_read -= 1
        if self.config.weather_forecast_data.index_read < 0:
            self.config.weather_forecast_data.index_read = len(self.config.weather_forecast_data.periods)-1
        self.update_UI_weather_forecast_data()
    """
    Cross-scene events:
        Events that occur within another scene that require changes to MainApplication QWidget.
    """
    def welcome_confirm_button_clicked(self):
        location_text = self.welcome_scene.location_text_box.text()
        if location_text == "":
            self.welcome_scene.guide.setText("Provide a location before pressing confirm.")
            return
        self.get_api_data_and_setup_ui(location_text, self.welcome_scene.guide, True)

    def settings_change_location_button_clicked(self):
        location_text = self.settings_scene.input_text_box.text()
        if location_text == "":
            self.settings_scene.error_label.setVisible(True)
            self.settings_scene.error_label.setText("Provide a location before pressing change location.")
            self.settings_scene.error_label.setStyleSheet("QLabel { color: #910700 }")
            return
        self.get_api_data_and_setup_ui(location_text, self.settings_scene.error_label)

    def settings_update_location_button_clicked(self):
        if self.config.successful_location_txt is None:
            self.settings_scene.error_label.setVisible(True)
            self.settings_scene.error_label.setText("You must have a location already before updating!")
            self.settings_scene.error_label.setStyleSheet("QLabel { color: #910700 }")
            return
        self.get_api_data_and_setup_ui(self.config.successful_location_txt, self.settings_scene.error_label)

    def get_api_data_and_setup_ui(self, location_text, result_obj, go_to_home_scene=False):
        """
        self.config.get_API_data > (error_code [0], msg [1])

        if return 1: unsuccessful
        if return 0: successful
        """
        result = self.config.get_API_data(location_text)
        result_obj.setVisible(True)
        if result[0] != 0:
            result_obj.setStyleSheet("QLabel { color: #910700 }")
            result_obj.setText(result[1])
            return

        # setup UI
        self.update_UI_geocode_data()
        self.update_UI_weather_forecast_data()
        self.update_UI_weather_forecast_hourly_data()
        self.update_UI_alerts_data()
        self.menu_button.setVisible(True)

        result_obj.setText("Success!")
        result_obj.setStyleSheet("QLabel { color: #218E00 }")

        if go_to_home_scene:
            self.request_change_scene("home_scene")

    def update_UI_geocode_data(self):
        self.home_scene.location_header.setText(self.config.geocode_data.get_location())

    def update_UI_weather_forecast_data(self):
        self.details_scene.temperature_high_display.setText("")
        self.details_scene.temperature_low_display.setText("")

        day_data = self.config.weather_forecast_data.get_period_from_index()
        extra_data = datetime.datetime.now() + datetime.timedelta(days=self.config.weather_forecast_data.index_read)
        extra_data = extra_data.strftime("%B %d")
        if int(extra_data[-1]) == 1 and int(extra_data[-2]) != 1:
            extra_data += "st"
        elif int(extra_data[-1]) == 2 and int(extra_data[-2]) != 1:
            extra_data += "nd"
        elif int(extra_data[-1]) == 3 and int(extra_data[-2]) != 1:
            extra_data += "rd"
        else:
            extra_data += "th"
        self.details_scene.day_display.setText(f"{day_data.name} - {extra_data}")
        self.details_scene.precipitation_chance_display.setText(f"precip {day_data.precipitation_probability}%")
        self.details_scene.wind_display.setText(f"{day_data.wind_speed} {day_data.wind_direction} winds")
        self.details_scene.forecasted_weather_display.setText(day_data.forecasted_weather)
        self.details_scene.precipitation_bar.setFixedHeight(int(((self.config.window_width//2)/100)*day_data.precipitation_probability))

        if day_data.high_temperature is not None:
            self.details_scene.temperature_high_display.setText(f"high temperature {day_data.high_temperature}°")
        if day_data.low_temperature is not None:
            self.details_scene.temperature_low_display.setText(f"low temperature {day_data.low_temperature}°")

    def update_UI_weather_forecast_hourly_data(self):
        current_hour = datetime.datetime.now().hour
        current_hour_data = None

        current_timezone_string = datetime.datetime.now(datetime.timezone.utc).astimezone()
        current_timezone_diff_utc = int(current_timezone_string.strftime("%z").strip('0'))

        for hour_data in self.config.weather_forecast_hourly_data.hours:
            if self.proper_hour(hour_data.hour, self.config.weather_forecast_hourly_data.timezone_utc_diff, current_timezone_diff_utc) == current_hour:
                current_hour_data = hour_data
        self.home_scene.temperature_display.setText(f"{current_hour_data.temperature}°")
        self.home_scene.forecast_display.setText(current_hour_data.forecasted_weather)
        self.home_scene.preciptation_display.setText(f"Precipitation: {current_hour_data.precipitation_probability}%")
        self.home_scene.wind_display.setText(f"Wind: {current_hour_data.wind_speed} {current_hour_data.wind_direction}")
        self.home_scene.message.setText(self.config.home_config.get_message_from_forecast(current_hour_data.forecasted_weather))

    def update_UI_alerts_data(self):
        self.warnings_scene.make_alerts(self.config.alerts_data, self.config.geocode_data)
    
    """
    Utility functions 
    """
    def request_change_scene(self, new_scene):
        if new_scene not in self.config.scenes_available:
            raise BaseException("SCENE NOT VALID")
        self.scenes.setCurrentIndex(self.config.scenes_available[new_scene])

    def proper_hour(self, data_hour, data_timezone, current_timezone_diff_utc):
        timezone_diff = current_timezone_diff_utc-data_timezone
        data_hour += timezone_diff
        if data_hour > 23:
            data_hour -= 23
        elif data_hour < 0:
            data_hour += 23
        return data_hour

app = QApplication([])

main_window = MainApplication()
#solves dilemma with text files randomly being open in other places
#filename = inspect.getframeinfo(inspect.currentframe()).filename
##path     = os.path.dirname(os.path.abspath(filename))
#print(path)
main_window.show()
app.exec()