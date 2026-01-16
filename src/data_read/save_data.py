import os

base_directory = os.path.dirname(__file__)
txt_file_directory = os.path.join(base_directory, "save_data.txt")

class SaveData:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.city = None
        self.state_name = None
        self.state_abbreviaton = None
        self.setup_file()

    def does_file_exist(self):
        return os.path.isfile(txt_file_directory)
    
    def setup_file(self):
        # read file instead
        if self.does_file_exist():
            with open(txt_file_directory, "r") as txt_file:
                geoposition_line = txt_file.readline()
                geopositions = [float(strnum.strip('\n').strip('\"')) for strnum in geoposition_line.split(" ")]
                self.latitude = geopositions[0]
                self.longitude = geopositions[1]

                city_line = txt_file.readline()
                city_line = city_line[city_line.find('\"'):].strip('\n').strip('\"')
                self.city = city_line if city_line != "None" else None

                state_name_line = txt_file.readline()
                state_name_line = state_name_line[state_name_line.find('\"'):].strip('\n').strip('\"')
                self.state_name = state_name_line if state_name_line != "{}" and state_name_line != "None" else None

                state_abbreviation_line = txt_file.readline()
                state_abbreviation_line = state_abbreviation_line[state_abbreviation_line.find('\"'):].strip('\n').strip('\"')
                self.state_abbreviaton = state_abbreviation_line if state_abbreviation_line != "{}" and state_abbreviation_line != "None" else None
        # make a new file
        else: 
            with open(txt_file_directory, "w") as txt_file:
                pass

    def location_exist(self):
        return self.latitude is not None and self.longitude is not None

    def save_data(self):
        with open(txt_file_directory, "w") as txt_file:
            txt_file.write(f'\"{self.latitude}\" \"{self.longitude}\"\n')
            txt_file.write(f'city \"{self.city}\"\n')
            txt_file.write(f'state_name \"{self.state_name}\"\n')
            txt_file.write(f'state_abbreviation \"{self.state_abbreviaton}\"\n')