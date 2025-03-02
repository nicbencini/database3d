"""
Contains functions for reading information from the SQLite database model.
"""
import sqlite3
import numpy as np
import json
from collections.abc import Iterable
import sys

class ReadMixin:

    def get_version(self):
        
        result = self.cursor.execute("SELECT * FROM model_info").fetchall()

        if len(result) == 0:
            return '0.0.0'

        return result[-1][0]
    
    
    def get(self, table_name, object_id):

        row_data = self.cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        column_names = [row[1] for row in row_data]

        types_data = self.cursor.execute(f"SELECT * FROM types_info WHERE table_name = ?",[table_name]).fetchone()[1]

        types_dictionary = json.loads(types_data)

        if '_id' in column_names:
        
            data = self.cursor.execute(f"SELECT * FROM {table_name} WHERE _id = ?",[object_id]).fetchone()
        else:
            data = self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 1 OFFSET ?", (object_id,)).fetchone()

        data = zip(column_names,data)

        attributes = []

        for attribute in data:

            attribute_name = attribute[0]
            attribute_value = attribute[1]
            attribute_type = types_dictionary[attribute_name][0]
            attribute_class = types_dictionary[attribute_name][1]

            if attribute_type == 'TEXT':
                attributes.append(attribute_value)
            elif attribute_type == 'INTEGER':
                attributes.append(int(attribute_value))
            elif attribute_type == 'FLOAT':
                attributes.append(float(attribute_value))
            elif attribute_type == 'BOOL':
                attributes.append(bool(attribute_value))
            elif attribute_type == 'ITER':
                attributes.append(json.loads(attribute_value))
            else:
                attributes.append(self.get(attribute_type,attribute_value))
        
        return attributes

    
    @staticmethod
    def get_class(class_name):
        for module_name, module in sys.modules.items():
            if module:  # Some modules might be None
                try:
                    if hasattr(module, class_name):
                        cls = getattr(module, class_name)
                        if isinstance(cls, type):  # Ensure it's a class
                            return cls, module_name
                except Exception:
                    pass  # Ignore any errors accessing attributes
        
        return None, None  # Class not found
   
    
    
    def get_pointload_count(self):

        query = f"SELECT COUNT(*) FROM load_pointload"

        return self.cursor.execute(query).fetchone()[0]

