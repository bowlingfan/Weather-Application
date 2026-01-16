from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QStackedWidget,
    QStackedLayout,
)
from scenes import (
    details_scene,
    welcome_scene,
    home_scene,
    warnings_scene,
    settings_scene,
    history_scene,
)
import configs.config as main_config
import configs.ui_config as ui_config
import datetime
#import inspect
#import os
        
class MainApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(ui_config.UI_Config["window"]["width"],ui_config.UI_Config["window"]["height"])
        self.setWindowTitle(ui_config.UI_Config["window"]["title"])
        self.data_files = main_config.DataFiles()

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

        self.scenes.setCurrentIndex(main_config.scenes_available["welcome_scene"])

        if self.data_files.save_data.location_exist():
            self.get_api_data_from_save_data_and_setup_ui(None,True)
    """
    Creating/Setup QT Window
    """
    def create_widgets(self):
        self.menu_widget = QWidget()
        self.menu_button_holder_widget = QWidget()
        self.menu_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["menu_button"]["default_txt"])

        self.home_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["home_button"]["default_txt"])
        self.warnings_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["warnings_button"]["default_txt"])
        self.details_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["details_button"]["default_txt"])
        self.settings_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["settings_button"]["default_txt"])
        self.history_button = ui_config.UI_Button(ui_config.UI_Non_Scene_Config["history_button"]["default_txt"])

        self.scenes = QStackedWidget()
        self.welcome_scene = welcome_scene.Scene()
        self.home_scene = home_scene.Scene()
        self.warnings_scene = warnings_scene.Scene()
        self.details_scene = details_scene.Scene()
        self.settings_scene = settings_scene.Scene()
        self.history_scene = history_scene.Scene()

    def design_widgets(self):
        self.menu_button.setMaximumSize(ui_config.UI_Non_Scene_Config["menu_button"]["maximum_size"])
        self.menu_button.setMinimumSize(ui_config.UI_Non_Scene_Config["menu_button"]["minimum_size"])
        self.menu_button_holder_widget.setMaximumSize(ui_config.UI_Non_Scene_Config["menu_button"]["holder_maximum_size"])
        self.menu_widget.setVisible(False)
        self.menu_button.setVisible(False)
        self.menu_widget.setMaximumWidth(ui_config.UI_Non_Scene_Config["menu_button"]["widget_holder_maximum_width"])

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
        self.scenes.addWidget(self.history_scene)
        """
        menu widget/button setup.

        local variables: menu_button_holder_layout & menu_widget_layout
        since they SHOULDN'T BE used other than to organize QT widgets.
        """
        menu_button_holder_layout = QVBoxLayout()
        menu_button_holder_layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        menu_button_holder_layout.setContentsMargins(ui_config.UI_Non_Scene_Config["menu_layout"]["holder_layout_margins"])
        menu_button_holder_layout.setSpacing(ui_config.UI_Non_Scene_Config["menu_layout"]["holder_layout_spacing"])
        menu_button_holder_layout.addWidget(self.menu_button)
        self.menu_button_holder_widget.setLayout(menu_button_holder_layout)

        menu_widget_layout = QVBoxLayout()
        menu_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignLeft)
        menu_widget_layout.setContentsMargins(ui_config.UI_Non_Scene_Config["menu_layout"]["widget_layout_margins"])
        menu_widget_layout.setSpacing(ui_config.UI_Non_Scene_Config["menu_layout"]["widget_layout_spacing"])
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
        self.data_files.weather_forecast_data.index_read += 1
        if self.data_files.weather_forecast_data.index_read >= len(self.data_files.weather_forecast_data.periods):
            self.data_files.weather_forecast_data.index_read = 0
        self.update_UI_weather_forecast_data()
    def decrement_button_clicked(self):
        self.data_files.weather_forecast_data.index_read -= 1
        if self.data_files.weather_forecast_data.index_read < 0:
            self.data_files.weather_forecast_data.index_read = len(self.data_files.weather_forecast_data.periods)-1
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
        if not self.data_files.save_data.location_exist():
            self.settings_scene.error_label.setVisible(True)
            self.settings_scene.error_label.setText("You must have a location already before updating!")
            self.settings_scene.error_label.setStyleSheet("QLabel { color: #910700 }")
            return
        self.get_api_data_from_save_data_and_setup_ui(self.settings_scene.error_label)

    def get_api_data_and_setup_ui(self, location_text, result_obj, go_to_home_scene=False):
        """
        self.config.get_API_data > (error_code [0], msg [1])

        if return 1: unsuccessful
        if return 0: successful
        """
        result = self.data_files.get_API_data(location_text)
        result_obj.setVisible(True)
        if result[0] != 0:
            result_obj.setStyleSheet("QLabel { color: #910700 }")
            result_obj.setText(result[1])
            return

        self.data_files.save_data.save_data()
        # setup UI
        self.setup_UI_with_data()

        result_obj.setText("Success!")
        result_obj.setStyleSheet("QLabel { color: #218E00 }")

        if go_to_home_scene:
            self.request_change_scene("home_scene")
    
    def get_api_data_from_save_data_and_setup_ui(self, result_obj=None, go_to_home_screen=False):
        latitude = self.data_files.save_data.latitude
        longitude = self.data_files.save_data.longitude

        if latitude is None or longitude is None:
            return
        
        if result_obj is None:
            result_obj = self.welcome_scene.guide

        result = self.data_files.get_weather_API_data(latitude, longitude)
        result_obj.setVisible(True)
        if result[0] != 0:
            result_obj.setStyleSheet("QLabel { color: #910700 }")
            result_obj.setText(result[1])
            return
        
        self.data_files.save_data.save_data()
        self.data_files.update_geocode_with_save()
        # setup UI
        self.setup_UI_with_data()
        
        result_obj.setText("Success!")
        result_obj.setStyleSheet("QLabel { color: #218E00 }")

        if go_to_home_screen:
            self.request_change_scene("home_scene")
        
    def setup_UI_with_data(self):
        self.update_UI_geocode_data()
        self.update_UI_weather_forecast_data()
        self.update_UI_weather_forecast_hourly_data()
        self.update_UI_alerts_data()
        self.menu_button.setVisible(True)

    def update_UI_geocode_data(self):
        self.home_scene.location_header.setText(self.data_files.geocode_data.get_location())

    def update_UI_weather_forecast_data(self):
        self.details_scene.temperature_high_display.setText("")
        self.details_scene.temperature_low_display.setText("")

        day_data = self.data_files.weather_forecast_data.get_period_from_index()
        extra_data = datetime.datetime.now() + datetime.timedelta(days=self.data_files.weather_forecast_data.index_read)
        # %B -> month $d -> day
        extra_data = main_config.format_month_day_based_on_timestr(extra_data.strftime("%B %d"))

        self.details_scene.day_display.setText(f"{day_data.name} - {extra_data}")
        self.details_scene.precipitation_chance_display.setText(f"precip {day_data.precipitation_probability}%")
        self.details_scene.wind_display.setText(f"{day_data.wind_speed} {day_data.wind_direction} winds")
        self.details_scene.forecasted_weather_display.setText(day_data.forecasted_weather)
        self.details_scene.precipitation_bar.setFixedHeight(main_config.number_from_percentage(ui_config.UI_Config["window"]["height"], day_data.precipitation_probability))

        if day_data.high_temperature is not None:
            self.details_scene.temperature_high_display.setText(f"high temperature {day_data.high_temperature}°")
        if day_data.low_temperature is not None:
            self.details_scene.temperature_low_display.setText(f"low temperature {day_data.low_temperature}°")

    def update_UI_weather_forecast_hourly_data(self):
        current_hour = datetime.datetime.now().hour
        current_hour_data = None

        current_timezone_string = datetime.datetime.now(datetime.timezone.utc).astimezone()
        current_timezone_diff_utc = int(current_timezone_string.strftime("%z").strip('0'))

        for hour_data in self.data_files.weather_forecast_hourly_data.hours:
            if main_config.convert_hour_with_timezone(hour_data.hour, self.data_files.weather_forecast_hourly_data.timezone_utc_diff, current_timezone_diff_utc) == current_hour:
                current_hour_data = hour_data

        self.home_scene.temperature_display.setText(f"{current_hour_data.temperature}°")
        self.home_scene.forecast_display.setText(current_hour_data.forecasted_weather)
        self.home_scene.preciptation_display.setText(f"Precipitation: {current_hour_data.precipitation_probability}%")
        self.home_scene.wind_display.setText(f"Wind: {current_hour_data.wind_speed} {current_hour_data.wind_direction}")
        self.home_scene.message.setText(main_config.get_home_message_from_forecast(current_hour_data.forecasted_weather))

        # sorry SQL thing
        self.data_files.history_database.exec_add_snapshot(main_config.get_proper_formatted_current_date(), self.data_files.geocode_data.get_location(), f"{datetime.datetime.now().time().strftime('%I:%M %p')} | UTC {current_timezone_diff_utc}", current_hour_data.temperature)
        print(self.data_files.history_database.get_database_data())
        
    def update_UI_alerts_data(self):
        self.warnings_scene.make_alerts(self.data_files.alerts_data, self.data_files.geocode_data)
    
    """
    Utility functions 
    """
    def request_change_scene(self, new_scene):
        if new_scene not in main_config.scenes_available:
            raise KeyError("SCENE NOT VALID")
        self.scenes.setCurrentIndex(main_config.scenes_available[new_scene])
app = QApplication([])
ui_config.make_font()

main_window = MainApplication()
main_window.show()
app.exec()