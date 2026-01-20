import os
import configs.config as main_config

class SaveData:
    def __init__(self, base_directory):
        self.latitude = None
        self.longitude = None
        self.city = None
        self.state_name = None
        self.state_abbreviaton = None
        self.base_directory = base_directory + "\\data_read"
        self.setup_file()
    
    def get_txt_file_directory(self):
        return self.base_directory + '\\save_data.txt'

    def does_file_exist(self):
        return os.path.isfile(self.get_txt_file_directory())
    
    def setup_file(self):
        # read file instead
        if self.does_file_exist():
            with open(self.get_txt_file_directory(), "r") as txt_file:
                # Ensure file is not empty
                if txt_file.read() == "":
                    return
                # Restores text file back to original position (at the top)
                txt_file.seek(0)

                geoposition_line = txt_file.readline()
                geopositions = [strnum.strip('\n').strip('\"') for strnum in geoposition_line.split(" ")]
                self.latitude = (-float(geopositions[0][1:])) if geopositions[0][0] == "-" else float(geopositions[0])
                self.longitude = (-float(geopositions[1][1:])) if geopositions[1][0] == "-" else float(geopositions[1])

                city_line = txt_file.readline()
                city_line = city_line[city_line.find('\"'):].strip('\n').strip('\"')
                self.city = city_line if city_line != "None" else None

                state_name_line = txt_file.readline()
                state_name_line = state_name_line[state_name_line.find('\"'):].strip('\n').strip('\"')
                self.state_name = state_name_line if type(state_name_line).__name__ != "dict" and state_name_line != "None" and state_name_line != "{}" else None

                state_abbreviation_line = txt_file.readline()
                state_abbreviation_line = state_abbreviation_line[state_abbreviation_line.find('\"'):].strip('\n').strip('\"')
                self.state_abbreviaton = state_abbreviation_line if type(state_name_line).__name__ != "dict" and state_abbreviation_line != "None" and state_abbreviation_line != "{}" else None
        # make a new file
        else: 
            with open(self.get_txt_file_directory(), "w") as txt_file:
                pass

    def location_exist(self):
        return self.latitude is not None and self.longitude is not None

    def save_data(self):
        with open(self.get_txt_file_directory(), "w") as txt_file:
            txt_file.write(f'\"{self.latitude}\" \"{self.longitude}\"\n')
            txt_file.write(f'city \"{self.city}\"\n')
            txt_file.write(f'state_name \"{self.state_name}\"\n')
            txt_file.write(f'state_abbreviation \"{self.state_abbreviaton}\"\n')