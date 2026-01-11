# read weather alerts data JSON and store in more readable format for use
import datetime

severe_ids = {
    "Severe": 2,
    "Moderate": 1,
}

class Alert():
    def __init__(self, feature_data):
        self.event_name = None
        self.expire_time = None
        self.description = None
        self.severity = None

        self.read_feature_data(feature_data)

    def read_feature_data(self, feature_data):
        self.event_name = feature_data['event']
        self.expire_time = self.convert_to_current_timezone(feature_data['expires'])
        self.description = feature_data['description'].replace('\n', ' ')
        self.severity = self.get_severity_id(feature_data['severity'])

    def convert_to_current_timezone(self, timestamp):
        current_timezone_string = datetime.datetime.now(datetime.timezone.utc).astimezone()
        current_timezone_diff_utc = int(current_timezone_string.strftime("%z").strip('0'))

        timestamp_diff_utc = int(timestamp[-6:].strip('0').strip(':'))
        hour = int(timestamp[timestamp.find('T')+1:timestamp.find('T')+3])
        hour = self.proper_hour(hour, timestamp_diff_utc, current_timezone_diff_utc)
        return hour
    
    def get_expire_time_in_datetime(self):
        return datetime.datetime.strptime(str(self.expire_time), "%H").strftime("%I:%M %p").strip('0')

    def get_severity_id(self, severity):
        return severe_ids[severity]
    
    def proper_hour(self, data_hour, data_timezone, current_timezone_diff_utc):
        timezone_diff = current_timezone_diff_utc-data_timezone
        data_hour += timezone_diff
        if data_hour > 23:
            data_hour -= 23
        elif data_hour < 0:
            data_hour += 23
        return data_hour
    
    def __str__(self):
        """
        DEBUG ONLY
        """
        return f"{self.event_name} - {self.severity}\nexpires approximately: {self.expire_time}\n{self.description}"

class AlertsData():
    def __init__(self, json):
        self.alerts = []
        self.read_json(json)
    def read_json(self, json):
        for feature in json['features']:
            new_alert = Alert(feature['properties'])
            self.alerts.append(new_alert)