import datetime
import json
from collections.abc import Iterable

class UpdateMixin:

    def update_version(self, increment):

        output = []

        current_version = self.get_version()

        version_values = [int(number) for number in current_version.split('.')]
        increment_value = [int(number) for number in increment.split('.')]

        for i,_ in enumerate(version_values):
            output.append(str(version_values[i] + increment_value[i]))
        
        return '.'.join(output)

    def update_logs(self, event_list):


        version_query = """
        INSERT INTO _model_log (
            version,
            user, 
            date,
            event) 
            VALUES 
            (?,?,?,?)
            """
        
        for event in event_list:
            version_value_string = (self.version,
                                    self.user,
                                    datetime.datetime.now(),
                                    event
                                    )

            self.cursor.execute(version_query, version_value_string)


    def update_model_info(self):
        """
        Adds a new model version
        
        Parameters:
        None

        Returns:
        None
        """     

        version_query = """
        INSERT INTO model_info (
            version,
            user, 
            date,  
            errors, 
            warnings, 
            run_time) 
            VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?)
            """

        version_value_string = (self.version,
                                self.user,
                                datetime.datetime.now(),
                                None, #TODO
                                None, #TODO
                                self.runtime
                                )

        self.cursor.execute(version_query, version_value_string)
    
    def update_object_paramter(self, table_name, object_id, parameter, new_value):

        column_names = self.get_table_columns(table_name)
        index_column = 'ROWID'

        if '_id' in column_names:
            index_column = '_id'
 
        update_query = f'UPDATE {table_name} SET {parameter} = ? WHERE {index_column} = ?;'

        if (isinstance(new_value, int) or 
            isinstance(new_value, float) or 
            isinstance(new_value, str) or
            isinstance(new_value, bool)
            ):
            attribute_value = str(new_value)     
            
        elif isinstance(new_value, Iterable):
            attribute_value = json.dumps(attribute_value)
        
        else:
            attribute_value = self.add(new_value)
     
        
        self.cursor.execute(update_query, (attribute_value, object_id))

        self.events.append(f'updated: {table_name} id = {object_id}')
    



    
    