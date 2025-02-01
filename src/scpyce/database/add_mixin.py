"""
Description
"""

import warnings
import sqlite3
import numpy as np
import datetime


class WriteMixin:

    def add_log(self, event_message):
        """
        Logs a model event.
        
        Parameters:
        None

        Returns:
        None
        """     

        cur = self.connection.cursor()

        version_query = """
        INSERT INTO model_log (
            version,
            user, 
            date,
            event) 
            VALUES 
            (?,?,?,?)
            """
        version_value_string = (self.version,
                                self.user,
                                datetime.datetime.now(),
                                event_message
                                )

        cur.execute(version_query, version_value_string)

        self.connection.commit()

        cur.close()

    def add_bar(self, bar, /, *, overwrite=False):
        """
        Adds a bar to the database. Returns the id of that bar. 
        If the bar already exists it will return the id of the existing bar
        and a warning will be returned.

        Adds the nodes of the start and end point of the bar to the table 
        if they do not already exist.

        Parameters:
        bar (bar object): The bar object to add to the database

        Returns:
        bar_id (string): The id of the added bar.
        """
        bar_id = None

        node_a_index = self.add_node(bar.node_a)
        node_b_index = self.add_node(bar.node_b)

        bar_check_query = """
            SELECT _id 
            FROM element_bar
            WHERE (node_a = ?)
            AND (node_b = ?)
            """
        
        bar_check_result = self.cursor.execute(bar_check_query,(node_a_index, node_b_index)).fetchone()

        if bar_check_result is not None:
            bar_id = bar_check_result[0]
            self.events.append(f'warning: bars merged at bar {bar_id}.')


        else:
            self.add_section(bar.section) # add section to database

            bar_query = """
            INSERT OR REPLACE INTO element_bar (
                _id, node_a, node_b, section, orientation_vector, release_a, release_b) 
                VALUES 
                (?,?,?,?,?,?,?)
                """

            bar_value_string = (bar.name,
                                node_a_index,
                                node_b_index,
                                bar.section.name,
                                np.array2string(bar.orientation_vector),
                                bar.release_a,
                                bar.release_b
                                )

            self.cursor.execute(bar_query, bar_value_string)

            bar_id = bar.name

            self.events.append(f'added: bar id = {bar_id}')


        return bar_id

   
    def add_node(self, node):
        """
        Adds a node to the database. Returns the id of that node. 
        If the node already exists it will return the id of the existing node.
        
        Parameters:
        node (node object): The node object to add to the database.

        Returns:
        node_index (int): The index of the added node.
        """

        node_index = None

        node_check_query = """
            SELECT _id
            FROM element_node
            WHERE (x = ?)
            AND (y = ?)
            AND (z = ?)
            """

        node_check_result = self.cursor.execute(node_check_query,(node.x, node.y, node.z)).fetchone()

        if node_check_result is not None:

            node_index = node_check_result[0]
            self.events.append(f'warning: nodes merged at node {node_index}.')


        else:

            node_index = self.cursor.execute("SELECT COUNT(*) FROM element_node").fetchone()[0]

            node_query = """
            INSERT INTO element_node (
                _id, x, y, z) 
                VALUES 
                (?,?,?,?)
                """

            node_value_string = (node_index, node.x, node.y, node.z)

            self.cursor.execute(node_query, node_value_string)

            self.events.append(f'added: node id = {node_index}')

        return node_index
    
    

    def add_material(self, material):
        """
        Adds a material to the database. Returns the name of that material. 
        If the material already exists it will return the name of the existing material.
        
        Parameters:
        material (material object): The material object to add to the database.

        Returns:
        material name (string): The name of the added material.
        """

        material_name = None

        material_check_query = """
            SELECT _id 
            FROM property_material
            WHERE (_id = ?)
            """

        material_check_result = self.cursor.execute(material_check_query,[material.name]).fetchone()

        if material_check_result is not None:

            material_name = material_check_result[0]
            self.events.append(f'warnging: material \'{material_name}\' already in database.')

        else:

            material_query = """
            INSERT INTO property_material (
                _id, youngs_modulus, poissons_ratio, shear_modulus, 
                coeff_thermal_expansion, damping_ratio,
                density, type, region, embodied_carbon) 
                VALUES 
                (?,?,?,?,?,?,?,?,?,?)
                """

            material_value_string = (material.name,
                                    material.youngs_modulus,
                                    material.poissons_ratio,
                                    material.shear_modulus,
                                    material.coeff_thermal_expansion,
                                    material.damping_ratio,
                                    material.density,
                                    material.type,
                                    material.region,
                                    material.embodied_carbon
                                    )

            self.cursor.execute(material_query, material_value_string)

            material_name = material.name

            self.events.append(f'added: material id = \'{material_name}\'')


        return material_name

    def add_section(self, section):
        """
        Adds a section to the database. Returns the name of that section. 
        If the section already exists it will return the name of the existing section.
        
        Parameters:
        section (section object): The section object to add to the database.

        Returns:
        section name (string): The name of the added section.
        """

        section_name = None

        section_check_query = """
            SELECT _id 
            FROM property_section
            WHERE (_id = ?)
            """

        section_check_result = self.cursor.execute(section_check_query, [section.name]).fetchone()

        if section_check_result is not None:

            section_name = section_check_result[0]
            self.events.append(f'warning: section \'{section_name}\' already in database.')

        else:

            self.add_material(section.material) # add material to database

            section_query = """
            INSERT INTO property_section (
                _id, material, area, izz, iyy) 
                VALUES 
                (?,?,?,?,?)
                """

            section_value_string = (section.name,
                                    section.material.name,
                                    section.area,
                                    section.izz,
                                    section.iyy
                                    )

            self.cursor.execute(section_query, section_value_string)

            section_name = section.name

            self.events.append(f'added: section id = \'{section_name}\'')
        

        return section_name

    def add_support(self, support):
        """
        Adds a support to the database. Returns the index of the node of the support. 
        If the node already exists it will return the id of the existing node.
        
        Parameters:
        support (support object): The support object to add to the database.

        Returns:
        node index (int): Index of support node.
        """

        node_index = None

        support_check_query = """
            SELECT node_index
            FROM element_support
            WHERE (node_index = ?)
            """

        node_index = self.add_node(support.node)

        support_check_result = self.cursor.execute(support_check_query, [node_index]).fetchone()

        if support_check_result is not None:

            support_index = support_check_result[0]
            self.events.append(f'warning: support merged at node \'{node_index}\'.')

        else:

            support_query = """
            INSERT INTO element_support (
                node_index, fx, fy, fz, mx, my, mz) 
                VALUES 
                (?,?,?,?,?,?,?)
                """

            support_value_string = (node_index,
                                    support.fx,
                                    support.fy,
                                    support.fz,
                                    support.mx,
                                    support.my,
                                    support.mz
                                    )

            self.cursor.execute(support_query, support_value_string)

            self.events.append(f'added: support id = {node_index}')

        return node_index

    def add_point_load(self, pointload):
        """
        Adds a point load to the database. Returns the index of the node of the point load. 
        If the node already exists it will return the index of the existing node.
        
        Parameters:
        pointload (pointload object): The pointload object to add to the database.

        Returns:
        node index (int): Index of point load node.
        """

        node_index = None

        pointload_check_query = """
            SELECT node_index
            FROM load_pointload
            WHERE (node_index = ?)
            """

        node_index = self.add_node(pointload.node)

        pointload_check_result = self.cursor.execute(pointload_check_query, [node_index]).fetchone()

        if pointload_check_result is not None:

            pointload_index = pointload_check_result[0]
            self.events.append(f'warning: load merged at node \'{node_index}\'.')

        else:

            pointload_query = """
            INSERT INTO load_pointload (
                node_index, fx, fy, fz, mx, my, mz) 
                VALUES 
                (?,?,?,?,?,?,?)
                """

            pointload_value_string = (node_index,
                                    pointload.fx,
                                    pointload.fy,
                                    pointload.fz,
                                    pointload.mx,
                                    pointload.my,
                                    pointload.mz
                                    )

            self.cursor.execute(pointload_query, pointload_value_string)

            self.events.append(f'added: point load id = {node_index}')

        return node_index


