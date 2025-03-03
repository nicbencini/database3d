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
    
    
    def test_add_object(self):

        node_1 = element.Node(0,0,0)
        node_2 = element.Node(0,0,1)

        bar = element.Bar(node_1, node_2, properties.Section.default(), [0,1,0], 'XXXXXX', 'XXXXXX', 'Test_Bar')


        self.structural_model.add(bar)
        self.structural_model.add(bar)
    
    def test_get_object(self):
        pass

        data = self.structural_model.get('bar', '1')
    

    def test_update_object_parameter_string(self):

        data = self.structural_model.update_object_paramter('bar', 1, 'section', 'new_material')

    def test_update_object_parameter_class(self):

        new_material = properties.Material('Concrete',263000,0.2,12000,0.00006,0,25,'Concrete')

        data = self.structural_model.update_object_paramter('bar', 2, 'section', new_material)
    
    def test_update_object_paramater_special_index(self):

        data = self.structural_model.update_object_paramter('material', 'steel', 'region', 'USA')

    def test_zdelete_object(self):
        pass
        
        #data = self.structural_model.delete_object('bar', 2)

    def tearDown(self):
        self.structural_model.close_connection()


if __name__ == '__main__':
    unittest.main()

