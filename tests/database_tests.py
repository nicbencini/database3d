"""
Tests for the object library.
"""

import os
import unittest
import numpy as np

from context import model # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error

class DatabaseTests(unittest.TestCase):
    """
    Tests for building the model database.
    """
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_7_model_test.db'
        
    def setUp(self):
        self.structural_model = model.Model(self.db_path, 'test_user', overwrite=False)
    

    def test_add_nodes(self):

        node = element.Node(1,2,3)
        add_node_result = self.structural_model.add_node(node)
        self.assertEqual(add_node_result,0)

    def test_add_bar(self):

        node_1 = element.Node(0,0,0)
        node_2 = element.Node(0,0,1)
        bar = element.Bar(node_1, node_2, properties.Section.default(), np.array([0,1,0]))

        add_bar_result = self.structural_model.add_bar(bar)

        self.assertIsNotNone(add_bar_result)
    

    @unittest.skip
    def test_build_database(self):
        """Builds the database for a pyramid strucutre."""

        self.structural_model.add_bar(bar1)
        self.structural_model.add_bar(bar2)
        self.structural_model.add_bar(bar3)
        self.structural_model.add_bar(bar4)

        self.structural_model.add_support(support1)
        self.structural_model.add_support(support2)
        self.structural_model.add_support(support3)
        self.structural_model.add_support(support4)

        self.structural_model.add_point_load(load1)

    @unittest.skip
    def test_get_material(self):
        """Test for getting material from the database."""

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
    def test_get_section(self):
        """Test for getting section from the database."""


        section = self.structural_model.get_section('UC305x305x97')

        self.assertEqual(section.name, 'UC305x305x97')
        self.assertEqual(section.material.name, 'steel')
        self.assertEqual(section.area, 0.0123)
        self.assertEqual(section.izz, 0.0002225)
        self.assertEqual(section.iyy, 7.308e-05)

    @unittest.skip
    def test_get_node(self):
        """Test for getting node from the database."""

        node = self.structural_model.get_node(3)

        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 1)
        self.assertEqual(node.z, 0)


    @unittest.skip
    def test_get_bar(self):
        """Test for getting bar from the database."""

        test_bar = self.structural_model.get_bar('5b324ddf-4c1e-42a1-b02a-4d9309498fb3')

    def tearDown(self):
        self.structural_model.close_connection()


if __name__ == '__main__':
    unittest.main()
