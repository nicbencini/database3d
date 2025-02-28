"""
Tests for the object library.
"""

import os
import unittest
import numpy as np

from context import model # pylint: disable=import-error
import element # pylint: disable=import-error
import properties
from datetime import datetime as dt


class DatabaseTests(unittest.TestCase):
    """
    Tests for building the model database.
    """
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ str(dt.now()) + '_test.db'
        
    def setUp(self):
        self.structural_model = model.Model(self.db_path, 'test_user', overwrite=False)
    
    @unittest.skip
    def test_build_info_table(self):

        self.structural_model.build_info_table()
        result = list(self.structural_model.cursor.execute("SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='model_info'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(model_info)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'version')
        self.assertEqual(columns[1][1], 'user')
        self.assertEqual(columns[2][1], 'date')
        self.assertEqual(columns[3][1], 'nodes')
        self.assertEqual(columns[4][1], 'bars')
        self.assertEqual(columns[5][1], 'sections')
        self.assertEqual(columns[6][1], 'materials')
        self.assertEqual(columns[7][1], 'loads')
        self.assertEqual(columns[8][1], 'supports')
        self.assertEqual(columns[9][1], 'errors')
        self.assertEqual(columns[10][1], 'warnings')
        self.assertEqual(columns[11][1], 'run_time')
    
    @unittest.skip
    def test_build_log_table(self):

        self.structural_model.build_log_table()
        result = list(self.structural_model.cursor.execute("SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='model_log'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(model_log)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'version')
        self.assertEqual(columns[1][1], 'user')
        self.assertEqual(columns[2][1], 'date')
        self.assertEqual(columns[3][1], 'event')

    @unittest.skip
    def test_build_bar_table(self):


        self.structural_model.build_bar_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='element_bar'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(element_bar)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], '_id')
        self.assertEqual(columns[1][1], 'node_a')
        self.assertEqual(columns[2][1], 'node_b')
        self.assertEqual(columns[3][1], 'section')
        self.assertEqual(columns[4][1], 'orientation_vector')
        self.assertEqual(columns[5][1], 'release_a')
        self.assertEqual(columns[6][1], 'release_b')
        self.assertEqual(columns[7][1], 'data')
    
    @unittest.skip
    def test_build_node_table(self):


        self.structural_model.build_node_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='element_node'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(element_node)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], '_id')
        self.assertEqual(columns[1][1], 'x')
        self.assertEqual(columns[2][1], 'y')
        self.assertEqual(columns[3][1], 'z')
        self.assertEqual(columns[4][1], 'data')
    
    @unittest.skip
    def test_build_support_table(self):

        self.structural_model.build_support_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='element_support'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(element_support)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'node_index')
        self.assertEqual(columns[1][1], 'fx')
        self.assertEqual(columns[2][1], 'fy')
        self.assertEqual(columns[3][1], 'fz')
        self.assertEqual(columns[4][1], 'mx')
        self.assertEqual(columns[5][1], 'my')
        self.assertEqual(columns[6][1], 'mz')
        self.assertEqual(columns[7][1], 'data')

    @unittest.skip
    def test_build_point_load_table(self):

        self.structural_model.build_support_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='load_pointload'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(load_pointload)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'node_index')
        self.assertEqual(columns[1][1], 'fx')
        self.assertEqual(columns[2][1], 'fy')
        self.assertEqual(columns[3][1], 'fz')
        self.assertEqual(columns[4][1], 'mx')
        self.assertEqual(columns[5][1], 'my')
        self.assertEqual(columns[6][1], 'mz')
    
    @unittest.skip
    def test_build_section_table(self):

        self.structural_model.build_support_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='property_section'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(property_section)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], '_id')
        self.assertEqual(columns[1][1], 'material')
        self.assertEqual(columns[2][1], 'area')
        self.assertEqual(columns[3][1], 'izz')
        self.assertEqual(columns[4][1], 'iyy')
    
    @unittest.skip
    def test_build_material_table(self):

        self.structural_model.build_material_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='property_material'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(property_material)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], '_id')
        self.assertEqual(columns[1][1], 'youngs_modulus')
        self.assertEqual(columns[2][1], 'poissons_ratio')
        self.assertEqual(columns[3][1], 'shear_modulus')
        self.assertEqual(columns[4][1], 'coeff_thermal_expansion')
        self.assertEqual(columns[5][1], 'damping_ratio')
        self.assertEqual(columns[6][1], 'density')
        self.assertEqual(columns[7][1], 'type')
        self.assertEqual(columns[8][1], 'region')
        self.assertEqual(columns[9][1], 'embodied_carbon')

    @unittest.skip
    def test_node_dispalcements_table(self):

        self.structural_model.build_node_displacements_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='result_node_displacement'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(result_node_displacement)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'node_index')
        self.assertEqual(columns[1][1], 'load_case')
        self.assertEqual(columns[2][1], 'ux')
        self.assertEqual(columns[3][1], 'uy')
        self.assertEqual(columns[4][1], 'uz')
        self.assertEqual(columns[5][1], 'rx')
        self.assertEqual(columns[6][1], 'ry')
        self.assertEqual(columns[7][1], 'rz')

    @unittest.skip
    def test_node_reactions_table(self):

        self.structural_model.build_node_reactions_table()
        result = list(self.structural_model.cursor.execute(f"SELECT name FROM sqlite_master " 
                                                      "WHERE type='table' " 
                                                      "AND name='result_node_reactions'"))

        columns = self.structural_model.cursor.execute(f"PRAGMA table_info(result_node_reactions)").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(columns[0][1], 'node_index')
        self.assertEqual(columns[1][1], 'load_case')
        self.assertEqual(columns[2][1], 'fx')
        self.assertEqual(columns[3][1], 'fy')
        self.assertEqual(columns[4][1], 'fz')
        self.assertEqual(columns[5][1], 'mx')
        self.assertEqual(columns[6][1], 'my')
        self.assertEqual(columns[7][1], 'mz')

    @unittest.skip
    def test_get_set_material(self):
        """Test for getting material from the database."""

        self.structural_model.add_material(properties.Material.default())

        material = self.structural_model.get_material('steel')

        self.assertEqual(material.name, 'steel')
        self.assertEqual(material.youngs_modulus, 210000.0)
        self.assertEqual(material.poissons_ratio, 0.3)
        self.assertEqual(material.shear_modulus, 76903.07)
        self.assertEqual(material.coeff_thermal_expansion, 1.17e-05)
        self.assertEqual(material.damping_ratio, 0.0)
        self.assertEqual(material.density, 76.9729)
        self.assertEqual(material.type, 'STEEL')
        self.assertEqual(material.region, 'UK')
        self.assertEqual(material.embodied_carbon, 12090.0)

    @unittest.skip
    def test_get_set_section(self):
        """Test for getting section from the database."""

        self.structural_model.add_section(properties.Section.default())

        section = self.structural_model.get_section('UC305x305x97')

        self.assertEqual(section.name, 'UC305x305x97')
        self.assertEqual(section.material.name, 'steel')
        self.assertEqual(section.area, 0.0123)
        self.assertEqual(section.izz, 0.0002225)
        self.assertEqual(section.iyy, 7.308e-05)

    @unittest.skip
    def test_get_set_node(self):
        """Test for getting node from the database."""

        node = element.Node(1,1,0)
        add_node_result = self.structural_model.add_node(node)
        
        node = self.structural_model.get_node(0)

        self.assertIsNotNone(add_node_result)
        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 1)
        self.assertEqual(node.z, 0)

    @unittest.skip
    def test_get_set_bar(self):
        """Test for getting bar from the database."""

        node_1 = element.Node(0,0,0)
        node_2 = element.Node(0,0,1)
        bar = element.Bar(node_1, node_2, properties.Section.default(), np.array([0,1,0]), 'XXXXXX', 'XXXXXX', 'Test_Bar')

        add_bar_result = self.structural_model.add_bar(bar)

        get_bar_result = self.structural_model.get_bar('Test_Bar')

        self.assertIsNotNone(add_bar_result)
        self.assertIsNotNone(get_bar_result)
    
    def test_add_object(self):

        node_1 = element.Node(0,0,0)
        node_2 = element.Node(0,0,1)
        #bar = element.Bar(node_1, node_2, properties.Section.default(), vector3d.Vector3d([0,1,0]), 'XXXXXX', 'XXXXXX', 'Test_Bar')

        bar = element.Bar(node_1, node_2, properties.Section.default(), [0,1,0], 'XXXXXX', 'XXXXXX', 'Test_Bar')

        self.structural_model.add(bar)
        self.structural_model.add(bar)
    
    def test_get_object(self):

        data = self.structural_model.get('bar', '1')

    def tearDown(self):
        self.structural_model.close_connection()


if __name__ == '__main__':
    unittest.main()
