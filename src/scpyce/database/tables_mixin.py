"""
Containse the functions for building the tables in the SQLite database model.
"""
import sqlite3

class TablesMixin:

    def build_tables(self):
        """
        Creates the following tables for the SQLite database model: 

        - nodes
        - bars
        - sections
        - materials
        - supports
        - loads
        - node reactions
        - node displacements

        Parameters:
        None

        Returns:
        None
        """

        #Build object tables
        self.build_info_table()
        self.build_log_table()
        self.build_bar_table()
        self.build_node_table()
        self.build_support_table()

        #Build property tables
        self.build_material_table()
        self.build_section_table()

        #Build load tables
        self.build_point_load_table()

        #Build results tables
        self.build_node_displacements_table()
        self.build_node_reactions_table()
    
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
            nodes INTEGER NOT NULL,
            bars INTEGER NOT NULL,
            sections INTEGER NOT NULL,
            materials INTEGER NOT NULL,
            loads INTEGER NOT NULL,
            supports INTEGER NOT NULL,
            errors TEXT,
            warnings TEXT,
            run_time FLOAT NOT NULL
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

    def build_bar_table(self):
        """
        Builds the bar table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        bar_table_schema = """
        CREATE TABLE IF NOT EXISTS element_bar (
            _id TEXT PRIMARY KEY,
            node_a INTEGER NOT NULL,
            node_b INTEGER NOT NULL,
            section TEXT NOT NULL,
            orientation_vector TEXT NOT NULL,
            release_a TEXT NOT NULL,
            release_b TEXT NOT NULL
            );
        """
        self.cursor.execute(bar_table_schema)

    def build_node_table(self):
        """
        Builds the node table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        node_table_schema = """
            CREATE TABLE IF NOT EXISTS element_node (
                _id INTEGER NOT NULL,
                x FLOAT NOT NULL,
                y FLOAT NOT NULL,
                z FLOAT NOT NULL
                );
            """
        self.cursor.execute(node_table_schema)

    def build_support_table(self):
        """
        Builds the support table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        support_table_schema = """
            CREATE TABLE IF NOT EXISTS element_support (
                node_index INTEGER NOT NULL PRIMARY KEY,
                fx INTEGER NOT NULL,
                fy INTEGER NOT NULL,
                fz INTEGER NOT NULL,
                mx INTEGER NOT NULL,
                my INTEGER NOT NULL,
                mz INTEGER NOT NULL
            );
            """
        self.cursor.execute(support_table_schema)


    def build_point_load_table(self):
        """
        Builds the point load table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        point_load_table_schema = """
            CREATE TABLE IF NOT EXISTS load_pointload (
                node_index INTEGER NOT NULL PRIMARY KEY,
                fx FLOAT NOT NULL,
                fy FLOAT NOT NULL,
                fz FLOAT NOT NULL,
                mx FLOAT NOT NULL,
                my FLOAT NOT NULL,
                mz FLOAT NOT NULL
            );
            """
        self.cursor.execute(point_load_table_schema)


    def build_section_table(self):
        """
        Builds the section table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        section_table_schema = """
            CREATE TABLE IF NOT EXISTS property_section (
                _id TEXT PRIMARY KEY,
                material TEXT NOT NULL,
                area FLOAT NOT NULL,
                izz FLOAT NOT NULL,
                iyy FLOAT NOT NULL
            );
            """
        self.cursor.execute(section_table_schema)

    def build_material_table(self):
        """
        Builds the material table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        material_table_schema = """
            CREATE TABLE IF NOT EXISTS property_material (
                _id TEXT PRIMARY KEY,
                youngs_modulus FLOAT NOT NULL,
                poissons_ratio FLOAT NOT NULL,
                shear_modulus FLOAT NOT NULL,
                coeff_thermal_expansion FLOAT NOT NULL,
                damping_ratio FLOAT NOT NULL,
                density FLOAT NOT NULL,
                type TEXT,
                region TEXT,
                embodied_carbon FLOAT
            );
            """
        self.cursor.execute(material_table_schema)

    def build_node_displacements_table(self):
        """
        Builds the node displacements table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        results_node_displacements = """
            CREATE TABLE IF NOT EXISTS result_node_displacement (
            node_index int NOT NULL,
            load_case string NOT NULL,
            ux float NOT NULL,
            uy float NOT NULL,
            uz float NOT NULL,
            rx float NOT NULL,
            ry float NOT NULL,
            rz float NOT NULL
            ); """

        self.cursor.execute(results_node_displacements)

    def build_node_reactions_table(self):
        """
        Builds the node displacements table for the model database.

        Parameters:
        connection (SQL connection): Connection to the model database.

        Returns:
        None
        """

        # create the database table if it doesn't exist
        results_node_reactions = """ CREATE TABLE IF NOT EXISTS
            result_node_reactions (
            node_index int NOT NULL,
            load_case string NOT NULL,
            fx float NOT NULL,
            fy float NOT NULL,
            fz float NOT NULL,
            mx float NOT NULL,
            my float NOT NULL,
            mz float NOT NULL
            ); """

        self.cursor.execute(results_node_reactions)
