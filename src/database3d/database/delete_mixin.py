

class DeleteMixin:

    def delete_object(self, table_name, object_id):
        
        column_names = self.get_table_columns(table_name)
        index_column = 'ROWID'

        if '_id' in column_names:
            index_column = '_id'

        delete_query = f'DELETE FROM {table_name} WHERE {index_column} = ?'
        
        self.cursor.execute(delete_query, (object_id,))

        self.events.append(f'deleted: {table_name} id = {object_id}')