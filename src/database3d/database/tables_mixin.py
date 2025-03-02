"""
Containse the functions for building the tables in the SQLite database model.
"""
import sqlite3
import json
from collections.abc import Iterable

class TablesMixin:

    def build_tables(self):
        """
        Creates the following tables for the SQLite database model: 

        - model_info
        - model_log

        Parameters:
        None

        Returns:
        None
        """

        #Build object tables
        self.build_info_table()
        self.build_log_table()
        self.build_types_table()
       
    
    def clear_all_tables(self):

        tables = self.get_tables()
        for table, in tables:
            #self.cursor.execute(f"DROP TABLE {table};")
            self.cursor.execute(f"DELETE FROM {table}")
        
    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type='table';")
        tables = self.cursor.fetchall()
        return tables

    def build_info_table(self):

        # create the database table if it doesn't exist
        info_table_schema = """
        CREATE TABLE IF NOT EXISTS model_info (
            version TEXT PRIMARY KEY,
            user TEXT NOT NULL,
            date timestamp NOT NULL,
            errors TEXT,
            warnings TEXT,
            run_time FLOAT NOT NULL
            );
        """
        self.cursor.execute(info_table_schema)

    def build_types_table(self):

        # create the database table if it doesn't exist
        info_table_schema = """
        CREATE TABLE IF NOT EXISTS types_info (
            table_name TEXT PRIMARY KEY,
            types TEXT NOT NULL
            );
        """
        self.cursor.execute(info_table_schema)

    def build_log_table(self):

        # create the database table if it doesn't exist
        table_schema = """
        CREATE TABLE IF NOT EXISTS model_log (
            version TEXT NOT NULL,
            user TEXT NOT NULL,
            date timestamp NOT NULL,
            event TEXT NOT NULL
            );
        """
        self.cursor.execute(table_schema)


    def build_object_table(self, model_object):

        table_name = model_object.__class__.__name__.lower()
        attribute_string = 'value TEXT'
        column_names = []
        types_dictionary = {}

        if hasattr(model_object, '__dict__') and len(model_object.__dict__) > 0:
            attribute_dictionary = model_object.__dict__
            attribute_string_list = []

            for attribute in attribute_dictionary.items():

                attribute_name = attribute[0].lower()
                attribute_value = attribute[1]
                attribute_value_type = 'NULL'
                primary_key = ''

                if isinstance(attribute_value, int):
                    attribute_value_type = 'INTEGER'
                    types_dictionary[attribute_name] = ('INTEGER',int.__name__)
                elif isinstance(attribute_value, float):
                    attribute_value_type = 'FLOAT'
                    types_dictionary[attribute_name] = ('FLOAT', float.__name__)
                elif isinstance(attribute_value, str):
                    attribute_value_type = 'TEXT'
                    types_dictionary[attribute_name] = ('TEXT', str.__name__)
                elif isinstance(attribute_value, bool):
                    attribute_value_type = 'BOOL'
                    types_dictionary[attribute_name] = ('BOOL', bool.__name__)
                elif isinstance(attribute_value, Iterable):
                    attribute_value_type = 'TEXT'
                    types_dictionary[attribute_name] = ('ITER' , type(attribute_value).__name__)
                else:
                    type_name = self.build_object_table(attribute_value)[0]
                    attribute_value_type = 'INTEGER'
                    types_dictionary[attribute_name] = (type_name, type(attribute_value).__name__)
                
                
                if attribute_name == '_id':
                    primary_key = ' NOT NULL PRIMARY KEY'

                column_names.append(attribute_name)
                attribute_string_list.append(f'{attribute_name} {attribute_value_type}{primary_key}')
            
            attribute_string = ','.join(attribute_string_list)

            query = f'INSERT OR IGNORE INTO types_info (table_name,types)VALUES(?,?)'
            values = [table_name, json.dumps(types_dictionary)]

            self.cursor.execute(query, values)
        
        table_schema = f'CREATE TABLE IF NOT EXISTS {table_name} (' + attribute_string + ');'

        self.cursor.execute(table_schema)

        return [table_name, column_names]
