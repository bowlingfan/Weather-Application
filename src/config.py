from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase
import requests
import random
from data_read.geocode_data import GeocodeData
from data_read.weather_forecast_data import WeatherForecastData
from data_read.weather_forecast_hourly_data import WeatherForecastHourlyData
"""
PRIVATE VARIABLES IF NOT IN class.__init__()
"""
default_font_directory = "resource/Roboto-Light.ttf"
"""
CLASSES/CONFIGS
"""
# °
class DetailsConfig():
    def __init__(self):
        pass
class WarningConfig():
    def __init__(self):
        self.no_weather_warning_messages = [
            "You're safe for this one."
        ]
class HomeConfig():
    forecast_msgs = {
        "sunny":[
            "Better hope the sun keeps up.",
            "Nice today, ain't it?",
            "It's your lucky day.. Mostly.",
            "Don't anticipate the continued sunniness.",
            "This is pretty boring. I hope the weather shakes up.",
        ],
        "light rain":{
            "Chance":[
                "An oddity.",
                "Don't you want a drizzle?",
                "Does some rain = cold?",
                "I wish it happened.",
            ],
            "NoChance":[
                "Do you feel the droplets pecking you?",
                "My favorite weather.",
                "Let the rain drop!",
                "It may get rougher. I hope it does. :)",
                "Wear a jacket. That might save you."
            ],
        },
        "rain":{
            "Chance":[
                "I don't think you'll like this one.",
                "How do you feel if I asked it to rain a bit harshly?",
                "Oh! Please let it fall!",
                "Might be a rough one. Prepare yourself!",
            ],
            "NoChance":[
                "Tip: REALLY wear a jacket.",
                "I heard acid is in the rain droplets, is that true?",
                "Weee! The grass will grow again!",
                "If you're disappointed, too bad.",
                "Tip: Stay inside. Or don't, take the advice."
            ],
        },
        "light snow":{
            "Chance":[
                "Okay, snowing.. a little too far.",
                "If you want me to stop it; how?",
                "Even though I'm delusional, I think this is a bad sign.",
            ],
            "NoChance":[
                "You won't cause a car accident, right?",
                "Don't slip. Wear boots. Simple.",
                "Probably ain't enough for a snowman, but for sure an ice angel!",
                "It hurts, a little bit.",
            ],
        },
        "snow":{
            "Chance":[
                "OKAY THIS IS SEVERE, I SHOULD HIBERNATE.",
                "Extremely cold soon.",
                "Is this Christmas at home?",
            ],
            "NoChance":[
                "[Weather APP failed to run.]",
                "AHHHHH!! IT HURTS! ITS FREEZING! I'M GETTING FROSTBITE!",
                "Be grateful it isn't a natural disaster.",
                "This, is just fine.",
            ],
        },
        "default":[
            "What am I even reading?",
            "Does not.. compute.",
            "Fake weather, don't believe it! (I'm kidding.)",
            "Special Weather perhaps.",
        ],
    }
    def __init__(self):
        self.temperature_display_font_size = 80
        
    def get_message_from_forecast(self, forecast):
        msgs = None
        forecast = forecast.lower()
        current_forecast = ""
        for forecast_possible in HomeConfig.forecast_msgs.keys():
            current_forecast = forecast_possible.lower()
            if current_forecast in forecast:
                msgs=HomeConfig.forecast_msgs[current_forecast]
                break
            if current_forecast == "default":
                msgs=HomeConfig.forecast_msgs[current_forecast]
                break
        if type(msgs).__name__ == "dict":
            if "chance" in current_forecast:
                current_forecast="Chance"
            else:
                current_forecast="NoChance"
            return random.choice(msgs[current_forecast])
        else:
            return random.choice(msgs)
class WelcomeConfig():
    def __init__(self):
        self.user_action_textbox_size = QSize(300,35)
        self.user_action_button_size = QSize(100,35)
class ConfigurationClass():
    def __init__(self):
        self.window_width=700

        self.scenes_available = {
            "welcome_scene":0,
            "home_scene":1,
            "warnings_scene":2,
            "details_scene":3
        }

        self.default_font_size = 15
        self.default_font_small_size = 8

        self.default_font = self.make_font(self.default_font_size)
        self.default_font_small = self.make_font(self.default_font_small_size)

        """
        base_url_api_geocoder -> {suggested location}?geoit=JSON
        base_url_api_weather -> {latitude},{longitude}

        check of the following:
        - error
        - throttled? (api limited)
        - must be in US due to NOAA limits
        """
        self.base_url_api_geocoder="https://geocode.xyz/"
        self.base_url_api_weather="https://api.weather.gov/points/"
        self.geocode_data=None
        self.weather_forecast_data=None
        self.weather_forecast_hourly_data=None

        #todo later
        self.alerts_data=None

        # configs for specific scenes
        self.welcome_config = WelcomeConfig()
        self.home_config = HomeConfig()
        self.warnings_config = WarningConfig()
    def make_default_QFont(self):
        """
        Returns QFont object with default settings.
        """
        qid = QFontDatabase.addApplicationFont(default_font_directory)
        # There is only 1 child font of the given Font Family.
        return QFont(QFontDatabase.applicationFontFamilies(qid)[0])
    def make_font(self, fontSize : int):
        font = self.make_default_QFont()
        font.setPointSize(fontSize)
        return font
    def get_API_data(self, suggested_location : str):
        """
        Returns (error_code [int], msg [str]) (type: tuple)
        enum error_code:
        - 3 | GEOCODE.XYZ exclusive | Province/Country must be US.
        - 2 |                       | Throttled API call.
        - 1 |                       | Error not listed in this docstring.
        - 0 | default               | successful

        msg [str] will be used to show as error msg for welcome_scene.guide QLabel.
        """
        # Multiple API calls to be stored for this variable.
        # geocode.xyz call to convert location to latt/longt coordinates.
        main_url = self.base_url_api_geocoder+suggested_location+"?geoit=JSON"
        api_call_holder = requests.get(main_url)

        geocode_data = api_call_holder.json()
        # Check Cases
        if 'error' in geocode_data:
            return (1,  f'An error occurred. Try a different location.')
        # for geocode specifically, if throttled occurs all JSON data is encoded to "Throttled! .
        # for this in particular we'll retry the call 5 times, if it fails, then kill/ask to retry.
        elif geocode_data['latt'][:len("Throttled!")] == "Throttled!":
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        elif geocode_data['standard']['prov'] != 'US':
            return (3, f'Location must be in the United States.')
        
        latitude=round(float(geocode_data['latt']),4)
        longitude=round(float(geocode_data['longt']),4)

        # Get location weather BASE data
        main_url=self.base_url_api_weather+f'{str(latitude)},{str(longitude)}'
        api_call_holder = requests.get(main_url)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()

        main_url=weather_forecast_data['properties']['forecast']
        main_url_2=weather_forecast_data['properties']['forecastHourly']

        # Get location weather FORECAST data
        api_call_holder = requests.get(main_url)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()

        # Get location weather FORECAST HOURLY data
        api_call_holder = requests.get(main_url_2)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_hourly_data = api_call_holder.json()

        # If no errors show up, assume successful and set class variables.
        self.geocode_data = GeocodeData(geocode_data)
        self.weather_forecast_data = WeatherForecastData(weather_forecast_data)
        self.weather_forecast_hourly_data = WeatherForecastHourlyData(weather_forecast_hourly_data)
        return (0, "")
