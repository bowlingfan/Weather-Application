
# todo write an error case for error when no internet..
import datetime
import requests, random
from data_read.geocode_data import GeocodeData
from data_read.weather_forecast_data import WeatherForecastData
from data_read.weather_forecast_hourly_data import WeatherForecastHourlyData
from data_read.alerts_data import AlertsData
from data_read.save_data import SaveData
from data_read.history_data import HistoryDatabase
import configs.msg_config as msg_config

"""
todo make a class to store all data variables.
use CLASS TITLE to reference them because cross-filing is restricted with namespacing
"""
scenes_available = {
    "welcome_scene":0,
    "home_scene":1,
    "warnings_scene":2,
    "details_scene":3,
    "settings_scene":4,
    "history_scene":5,
}

"""
base_url_api_geocoder -> {suggested location}?geoit=JSON
base_url_api_weather -> {latitude},{longitude}
base_url_api_alerts -> {zone}
"""
base_url_apis = {
    "geocode":"https://geocode.xyz/",
    "weather":"https://api.weather.gov/points/",
    "alerts": "https://api.weather.gov/alerts/active/zone/",
}

history_snapshot_limit = 30

geographical_position_decimal_places = 4
weather_alerts_throttled_status_code = 403

config = {
    "empty_txt": "",
    "get_api_data_success_code": 0,
    "maximum_hour_of_day": 23,
    "minimum_hour_of_day": 0,

    "database": {
        "name": "weather_history.db",
        "variables": ["id", "date", "location", "timestamp", "temperature"],
    },
}

months_to_number = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 1,
    "nov": 1,
    "dec": 1,
}

def number_from_percentage(main_data, percent):
    return int(main_data/100)*percent

def format_month_day_based_on_timestr(timestr):
    tens_place = int(timestr[-2])
    ones_place = int(timestr[-1])

    if ones_place == 1 and tens_place != 1:
        timestr += "st"
    elif ones_place == 2 and tens_place != 1:
        timestr += "nd"
    elif ones_place == 3 and tens_place != 1:
        timestr += "rd"
    else:
        timestr += "th"

    return timestr

def get_proper_formatted_current_date():
    current_date = datetime.datetime.now().date()
    month_day_str = format_month_day_based_on_timestr(current_date.strftime("%B %d"))
    year = current_date.strftime("%Y")
    return month_day_str + ", " + year

def convert_hour_with_timezone(input_hour, input_timezone, new_timezone):
    timezone_diff = new_timezone-input_timezone
    input_hour += timezone_diff
    if input_hour > config["maximum_hour_of_day"]:
        input_hour -= config["maximum_hour_of_day"]
    elif input_hour < config["minimum_hour_of_day"]:
        input_hour += config["maximum_hour_of_day"]
    return input_hour

def get_message_from_no_warnings():
    return random.choice(msg_config.no_weather_warning_messages)

def get_home_message_from_forecast(forecast):
    msgs = None
    forecast = forecast.lower()
    current_forecast = ""
    for forecast_possible in msg_config.forecast_messages.keys():
        current_forecast = forecast_possible.lower()
        if current_forecast in forecast:
            msgs=msg_config.forecast_messages[current_forecast]
            break
        if current_forecast == "default":
            msgs=msg_config.forecast_messages[current_forecast]
            break
    # If there is a Chance/NoChance property for current_forecast
    if type(msgs).__name__ == "dict":
        if "chance" in forecast.lower():
            current_forecast="Chance"
        else:
            current_forecast="NoChance"
        return random.choice(msgs[current_forecast])
    else:
        return random.choice(msgs)
    
def convert_datestr_to_data(datestr : str):
    """
    returns tuple of all INTs:
        day, month, year
        respectively.
    """
    data = datestr.split(' ')
    month_num = months_to_number[data[0].lower()[0:3]]
    day_num = int(data[1][0:2])
    year_num = int(data[2])
    return (day_num, month_num, year_num)

def snapshot_already_taken(recent_snapshot_date):
    recent_snapshot_date_data = convert_datestr_to_data(recent_snapshot_date)

    current_datetime = datetime.datetime.now().date()
    current_day = current_datetime.day
    current_month = current_datetime.month
    current_year = current_datetime.year

    return current_day == recent_snapshot_date_data[0] and current_month == recent_snapshot_date_data[1] and current_year == recent_snapshot_date_data[2]

class DataFiles:
    def __init__(self):
        self.geocode_data : GeocodeData = None
        self.weather_forecast_data : WeatherForecastData = None
        self.weather_forecast_hourly_data : WeatherForecastHourlyData = None
        self.successful_location_txt : str = None # todo save data
        self.alerts_data : AlertsData = None
        self.save_data : SaveData = SaveData()
        self.history_database : HistoryDatabase = HistoryDatabase()

    def update_geocode_with_save(self):
        self.geocode_data = GeocodeData()
        self.geocode_data.city = self.save_data.city
        self.geocode_data.state_name = self.save_data.state_name
        self.geocode_data.state_abbreviaton = self.save_data.state_abbreviaton

    def exec_delete_query(self, id):
        self.history_database.exec_query("remove_snapshot", id)

    # Helper Function
    def get_API_data(self, suggested_location : str):
        return self.get_geocode_API_data(suggested_location)
    
    def get_geocode_API_data(self, suggested_location : str):
        """
        Returns (error_code [int], msg [str]) (type: tuple)
        enum error_code:
        - 3 | GEOCODE.XYZ exclusive | Province/Country must be US.
        - 2 |                       | Throttled API call.
        - 1 |                       | Error not listed in this docstring.
        - 0 | default               | successful
        msg [str] will be used to show as error msg for welcome_scene.guide QLabel.
        """
        # geocode.xyz call to convert location to latt/longt coordinates.
        geocode_url = base_url_apis["geocode"]+suggested_location+"?geoit=JSON"
        try:
            api_call_holder = requests.get(geocode_url)
        except:
            return (1,  f'An error occurred. Maybe no internet connection?')
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
        
        latitude=round(float(geocode_data['latt']), geographical_position_decimal_places)
        longitude=round(float(geocode_data['longt']), geographical_position_decimal_places)

        self.geocode_data = GeocodeData(geocode_data)
        self.save_data.latitude = latitude
        self.save_data.longitude = longitude
        self.save_data.city = self.geocode_data.city
        self.save_data.state_name = self.geocode_data.state_name
        self.save_data.state_abbreviaton = self.geocode_data.state_abbreviaton
        
        return self.get_weather_API_data(latitude, longitude)
    
    def get_weather_API_data(self, latitude, longitude):
        # Get location weather BASE data
        weather_base_url = base_url_apis["weather"]+f'{str(latitude)},{str(longitude)}'
        try:
            api_call_holder = requests.get(weather_base_url)
        except:
            return (1,  f'An error occurred. Maybe no internet connection?')
        # Throttled Error Case
        if api_call_holder.status_code == weather_alerts_throttled_status_code:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()

        # Make URLs
        forecast_url = weather_forecast_data['properties']['forecast']
        forecast_hourly_url = weather_forecast_data['properties']['forecastHourly']
        # get zone first then make url.
        alerts_url = weather_forecast_data['properties']['forecastZone']
        alerts_url = base_url_apis["alerts"] + alerts_url[alerts_url.find('/',-10)+1:]
        
        # Get location weather FORECAST data
        try:
            api_call_holder = requests.get(forecast_url)
        except:
            return (1,  f'An error occurred. Maybe no internet connection?')
        # Throttled Error Case
        if api_call_holder.status_code == weather_alerts_throttled_status_code:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()
        
        # Get location weather FORECAST HOURLY data
        try:
            api_call_holder = requests.get(forecast_hourly_url)
        except:
            return (1,  f'An error occurred. Maybe no internet connection?')
        # Throttled Error Case
        if api_call_holder.status_code == weather_alerts_throttled_status_code:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_hourly_data = api_call_holder.json()
        
        # Get location forecast ALERTS data
        try:
            api_call_holder = requests.get(alerts_url)
        except:
            return (1,  f'An error occurred. Maybe no internet connection?')
        # Throttled Error Case
        if api_call_holder.status_code == weather_alerts_throttled_status_code:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        alerts_data = api_call_holder.json()
        
        # If no errors show up, assume successful and set class variables.
        self.weather_forecast_data = WeatherForecastData(weather_forecast_data)
        self.weather_forecast_hourly_data = WeatherForecastHourlyData(weather_forecast_hourly_data)
        self.alerts_data = AlertsData(alerts_data)
        return (0, "")