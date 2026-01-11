# read weather forecasted JSON and store in more readable format for use
import datetime
class Period():
    def __init__(self):
        """
        Docstring for __init__
        
        name: str
        high_temperature: number (int)
        low_temperature: number (int)
        precipitation_probability: tuple > number (float)
        wind_speed: str
        wind_direction: str 
        forecasted_weather: str 
        """
        self.name = None
        self.high_temperature = None
        self.low_temperature = None
        self.precipitation_probability = None
        self.wind_speed = None
        self.wind_direction = None
        self.forecasted_weather = None

    def read_day_period(self, day_period):
        self.high_temperature = day_period['temperature']
        self.precipitation_probability = day_period['probabilityOfPrecipitation']['value']
        self.wind_speed = day_period['windSpeed']
        self.wind_direction = day_period['windDirection']
        self.forecasted_weather = day_period['shortForecast']

    def read_night_period(self, night_period):
        self.low_temperature = night_period['temperature']
        if self.precipitation_probability is None:
            self.precipitation_probability = night_period['probabilityOfPrecipitation']['value']
        if self.wind_speed is None:
            self.wind_speed = night_period['windSpeed']
        if self.wind_direction is None:
            self.wind_direction = night_period['windDirection']
        if self.forecasted_weather is None:
            self.forecasted_weather = night_period['shortForecast']

    def __str__(self):
        """
        DEBUG ONLY
        """
        return f"day_name: {self.name}\ntemps: {self.low_temperature} - {self.high_temperature}\nprecip: {self.precipitation_probability}\nwind: {self.wind_speed} {self.wind_direction}\nforecast: {self.forecasted_weather}\n"
class WeatherForecastData():
    def __init__(self, json):
        self.periods = []
        self.index_read = 0
        self.read_json(json)
    def read_json(self, json):
        periods = json['properties']['periods']
        #print(periods)
        # we have the same day next week from API data.
        if periods[0]['name'] == 'Tonight':
            day_name = datetime.datetime.now()
            first_day_period = Period()
            first_day_period.read_night_period(periods[0])
            first_day_period.name = day_name.strftime("%A")
            self.periods.append(first_day_period)

            for index in range(1,len(periods)//2):
                day_name = datetime.datetime.now() + datetime.timedelta(days=index)
                current_period = Period()
                current_period.read_day_period(periods[index*2-1])
                current_period.read_night_period(periods[index*2])
                current_period.name = day_name.strftime("%A")
                self.periods.append(current_period)

            day_name = datetime.datetime.now() + datetime.timedelta(days=8)
            last_day_period = Period()
            last_day_period.read_day_period(periods[0])
            last_day_period.name = day_name.strftime("%A")
            self.periods.append(last_day_period)
        else:
            for index in range(len(periods)//2):
                day_name = datetime.datetime.now() + datetime.timedelta(days=index)
                current_period = Period()
                current_period.read_day_period(periods[index*2])
                current_period.read_night_period(periods[index*2+1])
                current_period.name = day_name.strftime("%A")
                self.periods.append(current_period)
    def get_period_from_index(self):
        return self.periods[self.index_read]