# read weather forecasted hourly JSON and store in more readable format for use
import datetime
class HourData():
    def __init__(self):
        """
        Docstring for __init__
        
        hour: number (int)
        temperature: number (int)
        precipitation_probability: tuple > number (float)
        wind_speed: str
        wind_direction: str 
        forecasted_weather: str 
        """
        self.hour = None
        self.temperature = None
        self.precipitation_probability = None
        self.wind_speed = None
        self.wind_direction = None
        self.forecasted_weather = None

    def read_hour_data(self,data):
        self.temperature = data['temperature']
        self.precipitation_probability = data['probabilityOfPrecipitation']['value']
        self.wind_speed = data['windSpeed']
        self.wind_direction = data['windDirection']
        self.forecasted_weather = data['shortForecast']

    def __str__(self):
        """
        DEBUG ONLY
        """
        return f"hour: {self.hour}\ntemperature: {self.temperature}\nprecipitation: {self.precipitation_probability}\nwind: {self.wind_speed} {self.wind_direction}\nforecast: {self.forecasted_weather}\n"

class WeatherForecastHourlyData():
    def __init__(self, json):
        self.hours = []
        self.timezone_utc_diff = 0
        self.read_json(json)
    def read_json(self, json):
        current_day = datetime.datetime.now().day
        periods = json['properties']['periods']
        end_index = self.index_of_end_current_day(current_day, periods)
        self.timezone_utc_diff = int(periods[0]['startTime'][-6:].strip('0').strip(':'))

        for index in range(end_index):
            period = periods[index]

            hour_data = HourData()
            hour_data.hour = 24-end_index+index
            hour_data.read_hour_data(period)

            self.hours.append(hour_data)
    def index_of_end_current_day(self, current_day, periods):
        index=0
        for period in periods:
            startTime : str = period['startTime'] 
            second_dash_index = startTime.index("-",startTime.index("-")+1)
            t_index = startTime.index("T")
            startDay = int(startTime[second_dash_index+1:t_index])
            if startDay!=current_day:
                return index
            index += 1
        return -1