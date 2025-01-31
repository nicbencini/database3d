"""
Contains the Model class for building and modifying the structural SQLite database 
model which contains the geometrical and structural data used by the solver. 

Results from the solver are stored in the model database after the solver is run.

This module references the tables.py, read.py and write.py modules for reading and 
modifying the database model.

"""

import sqlite3
import datetime

from . import tables_mixin # pylint: disable=import-error
from . import write_mixin # pylint: disable=import-error
from . import read_mixin # pylint: disable=import-error

class Model(tables_mixin.TablesMixin, write_mixin.WriteMixin, read_mixin.ReadMixin):
    """
    Used for creating the tables for the database model and 
    reading and writing into the databse. 

    The Model class contains the variable for the file path to the model
    and the SQLite connection.

    IMPORTANT: 
    - The build_tables method must be run to create the model tables before
    data is stored in the model. 
    -The close_connection method must be run to end work
    on the model and close the connection to the SQLite database.
    """
    def __init__(self , file_path, user):
        self.database_path = file_path
        self.connection = sqlite3.connect(self.database_path)
        self.user = user
        self.errors = None
        self.warnings = None
        self.runtime = 0

        print(f'Connected to {self.database_path}')
    
    def update_version(self):
        """
        Adds a new model version
        
        Parameters:
        None

        Returns:
        None
        """     

        cur = self.connection.cursor()

        version_query = """
        INSERT INTO model_info (
            user, 
            date, 
            nodes, 
            bars, 
            sections, 
            materials, 
            loads, 
            supports, 
            errors, 
            warnings, 
            run_time) 
            VALUES 
            (?,?,?,?,?,?,?,?,?,?,?)
            """

        version_value_string = (self.user,
                                datetime.datetime.now(),
                                self.get_node_count(),
                                self.get_bar_count(),
                                self.get_section_count(),
                                self.get_material_count(),
                                self.get_pointload_count(),
                                self.get_support_count(),
                                self.errors,
                                self.warnings,
                                self.runtime
                                )

        cur.execute(version_query, version_value_string)

        self.connection.commit()

        cur.close()

    def close_connection(self):
        """
        Closes the connection to the model database.
        
        Parameters:
        None

        Returns:
        None        
        """

        self.update_version()

        self.connection.close()
        print( f'Connection to {self.database_path} closed')
    
    
