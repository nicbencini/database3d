"""
Contains functions for reading information from the SQLite database model.
"""
import sqlite3
import numpy as np
import json
from collections.abc import Iterable

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
            attribute_type = types_dictionary[attribute_name]

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



    
    
    """
    def get_bar(self, bar_name):


        bar_data = self.cursor.execute("SELECT * FROM element_bar WHERE _id = ?",[bar_name]).fetchone()
        bar_data = list(bar_data)

        id = bar_data[0]
        node_a = self.get_node(bar_data[1])
        node_b = self.get_node(bar_data[2])
        section = self.get_section(bar_data[3])

        orientation_vector = str.replace(bar_data[4],'[','')
        orientation_vector = str.replace(orientation_vector,']','')
        orientation_vector = str.split(orientation_vector,' ')

        orientation_vector = np.array([float(orientation_vector[0]),
                                        float(orientation_vector[1]),
                                        float(orientation_vector[2])]
                                        )

        release_a = bar_data[5]
        release_b = bar_data[6]

        bar_data = bar_data[7]

        bar_object = element.Bar(node_a,
                                    node_b,
                                    section,
                                    orientation_vector,
                                    release_a,
                                    release_b,
                                    id,
                                    bar_data)

        return bar_object
    """
    
    
    def get_pointload_count(self):

        query = f"SELECT COUNT(*) FROM load_pointload"

        return self.cursor.execute(query).fetchone()[0]

