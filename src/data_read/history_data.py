from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import configs.config as main_config
import os

"""
PRIVATE VARIABLES
"""
base_directory = os.path.dirname(__file__)
sql_folder_directory = "sql" # as add on to base_directory
"""
refer to SQL folder from working project if needed.
"""
sql_queries = {}

class HistoryDatabase:
    def __init__(self):
        self.database = None
        self.database_usable = False
        self.lowest_id_existent = 1
        self.database_record_size = 0

        self.setup_database()
        self.exec_query("setup_table")

    def setup_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(main_config.config["database"]["name"])
        self.is_database_open()
        self.get_database_data() # get database_record_size
    
    def is_database_open(self):
        self.database_usable = self.database.open()
        return self.database_usable
    
    def translate_bind_values_to_list(self, bind_values):
        if len(bind_values) < 1:
            return bind_values
        listed_parameters = list(bind_values)
        return listed_parameters

    def exec_query(self, command_key, *bind_values):
        if not self.database_usable:
            print("WARNING: Database not open. Error occurred from opening.\n"); return
        if command_key not in sql_queries:
            print("WARNING: MUST HAVE VALID SQL QUERY NAME."); return
        with open(os.path.join(base_directory, sql_folder_directory, sql_queries[command_key])) as opened_sql_file:
            query = QSqlQuery()
            query.prepare(opened_sql_file.read())
            for bind_value in self.translate_bind_values_to_list(bind_values):
                query.addBindValue(bind_value)    
            query.exec()
            return query
    
    # helper function
    def exec_add_snapshot(self, *bind_values):
        if self.database_record_size > 3:
            self.database_record_size -= 1
            self.exec_query("remove_snapshot", self.lowest_id_existent)

        self.exec_query("add_snapshot", *bind_values)
        self.database_record_size += 1

    def get_database_data(self):
        result=[]
        query = self.exec_query("read_data")
        amt = 0
        while query.next():
            data={}
            amt += 1
            for index, key in enumerate(main_config.config["database"]["variables"]):
                queried_value_from_index = query.value(index)
                if amt == 1 and key == "id":
                    self.lowest_id_existent = queried_value_from_index
                data.update({key:queried_value_from_index})
            result.append(data)
        self.database_record_size = amt
        return result
    
    def display_all_sql_directories(self):
        """
        PRINTS ALL SQL FILES POSSIBLE FOR USE. DOES NOT RETURN THEM.
        """
        print("QUERIES ---------")
        print(f"Given folder: {str(os.path.join(base_directory,sql_folder_directory))}")
        index = 0
        for sql_query_name, sql_query_name_with_extension in sql_queries.items():
            print(f"* {index}: {sql_query_name} --> {sql_query_name_with_extension}")
            index += 1

def setup_sql_directories():
    for sql_query_name in os.listdir(os.path.join(base_directory,sql_folder_directory)):
        no_extension_name=sql_query_name[0:sql_query_name.index('.')]
        sql_queries.update({no_extension_name:sql_query_name})

setup_sql_directories()
