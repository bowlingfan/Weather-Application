from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from config import HistoryDataConfig
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
        self.data_config = HistoryDataConfig()
        self.database = None
        self.database_usable = False

        self.setup_database()
        self.exec_query("setup_table")

    def setup_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(self.data_config.database_name)
        self.is_database_open()
    
    def is_database_open(self):
        self.database_usable = self.database.open()
        return self.database_usable
    
    def exec_query(self, command_key, *bind_values):
        if not self.database_usable:
            print("WARNING: Database not open. Error occurred from opening.\n"); return
        if command_key not in sql_queries:
            print("WARNING: MUST HAVE VALID SQL QUERY NAME."); return
        with open(os.path.join(base_directory, sql_folder_directory, sql_queries[command_key])) as opened_sql_file:
            query = QSqlQuery()
            query.prepare(opened_sql_file.read())
            for bind_value in bind_values:
                query.addBindValue(bind_value)
            query.exec()

    def get_query_result(self):
        result=[]
        query = self.exec_query("read_data")
        while query.next():
            data={}
            for index, key in enumerate(self.data_config.database_variables):
                data.update({key:query.value(index)})
            result.append(data)
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
