# read geocode JSON and store in more readable format for use

class GeocodeData():
    def __init__(self, json=None):
        self.city = None
        self.state_name = None
        self.state_abbreviaton = None
        if json is not None:
            self.read_std(json['standard'])
    def read_std(self, std_data):
        self.city = std_data["city"]
        self.state_abbreviaton = std_data["statename"]
        self.state_name = std_data["addresst"]
    def get_location(self):
        state_abbreviaton_is_dict = type(self.state_abbreviaton).__name__ == "dict"
        state_name_is_dict = type(self.state_name).__name__ == "dict"

        if state_abbreviaton_is_dict and state_name_is_dict:
            return f"{self.city}"
        elif state_name_is_dict:
            return f"{self.city}, {self.state_abbreviaton}"
        else:
            return f"{self.city}, {self.state_name}"
    def __str__(self):
        return self.get_location() + f" ({self.state_name}, {self.state_abbreviaton})"