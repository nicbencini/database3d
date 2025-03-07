"""
Tests for the object library.
"""

import os
import unittest
import numpy as np
import string

from context import model  # pylint: disable=import-error
from datetime import datetime as dt
from test_object import TestObject, TestProperty, TestSubproperty  # pylint: disable=import-error
import random


class DatabaseTests(unittest.TestCase):
    """
    Tests for building the model database.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class by creating a database path.
        """
        cls.db_path = os.path.dirname(os.path.realpath(__file__)) + '/test_files/' + str(dt.now()) + '_test.db'

    def setUp(self):
        """
        Set up the test case by initializing the model and creating a test object.
        """
        self.test_database = model.Model(self.db_path, 'test_user', overwrite=False)
        
        subproperty = TestSubproperty(
            random.randint(1, 100),
            random.randint(1, 100),
            random.randint(1, 100)
        )
        
        random_string = ''.join(random.choices(string.ascii_letters, k=10))
        
        property_instance = TestProperty(
            random_string,
            random.randint(1, 100),
            subproperty
        )
        
        self.test_object = TestObject(
            random.randint(1, 100),
            random_string,
            random.choice([True, False]),
            [random.randint(1, 100) for _ in range(5)],
            {"key": "value"},
            random_string,
            property_instance
        )
    
    def test_add_object(self):
        """
        Test adding an object to the database and retrieving it.
        """
        self.test_database.add(self.test_object)
        retrieved_object = self.test_database.get('testobject', self.test_object._id)
        
        self.assertIsNotNone(retrieved_object)
        self.assertEqual(retrieved_object._id, self.test_object._id)
        self.assertEqual(retrieved_object.integer, self.test_object.integer)
        self.assertEqual(retrieved_object.string, self.test_object.string)
        self.assertEqual(retrieved_object.boolean, self.test_object.boolean)
        self.assertEqual(retrieved_object.list_param, self.test_object.list_param)
        self.assertEqual(retrieved_object.dict_param, self.test_object.dict_param)
        self.assertEqual(retrieved_object.class_object.string, self.test_object.class_object.string)
        self.assertEqual(retrieved_object.class_object.integer, self.test_object.class_object.integer)
        self.assertEqual(retrieved_object.class_object.class_object.int1, self.test_object.class_object.class_object.int1)
        self.assertEqual(retrieved_object.class_object.class_object.int2, self.test_object.class_object.class_object.int2)
        self.assertEqual(retrieved_object.class_object.class_object.int3, self.test_object.class_object.class_object.int3)

    @unittest.skip
    def test_update_object_parameter_string(self):
        """
        Test updating an object parameter with a string value.
        """
        self.test_database.add(self.test_object)
        new_string = ''.join(random.choices(string.ascii_letters, k=10))
        self.test_database.update_object_paramter('testobject', self.test_object._id, 'string', new_string)
        
        updated_object = self.test_database.get('testobject', self.test_object._id)
        self.assertEqual(updated_object.string, new_string)

    @unittest.skip
    def test_update_object_parameter_class(self):
        """
        Test updating an object parameter with a class instance.
        """
        self.test_database.add(self.test_object)
        new_subproperty = TestSubproperty(
            random.randint(1, 100),
            random.randint(1, 100),
            random.randint(1, 100)
        )
        new_property_instance = TestProperty(
            ''.join(random.choices(string.ascii_letters, k=10)),
            random.randint(1, 100),
            new_subproperty
        )
        self.test_database.update_object_paramter('testobject', self.test_object._id, 'class_object', new_property_instance)
        
        updated_object = self.test_database.get('testobject', self.test_object._id)
        self.assertEqual(updated_object.class_object.string, new_property_instance.string)
        self.assertEqual(updated_object.class_object.integer, new_property_instance.integer)
        self.assertEqual(updated_object.class_object.class_object.int1, new_property_instance.class_object.int1)
        self.assertEqual(updated_object.class_object.class_object.int2, new_property_instance.class_object.int2)
        self.assertEqual(updated_object.class_object.class_object.int3, new_property_instance.class_object.int3)

    @unittest.skip
    def test_update_object_paramater_special_index(self):
        """
        Test updating an object parameter with a special index.
        """
        self.test_database.add(self.test_object)
        new_region = ''.join(random.choices(string.ascii_letters, k=10))
        self.test_database.update_object_paramter('testobject', self.test_object._id, 'dict_param', {"region": new_region})
        
        updated_object = self.test_database.get('testobject', self.test_object._id)
        self.assertEqual(updated_object.dict_param["region"], new_region)

    @unittest.skip
    def test_delete_object(self):
        """
        Test deleting an object from the database.
        """
        self.test_database.add(self.test_object)
        self.test_database.delete_object('testobject', self.test_object._id)
        
        deleted_object = self.test_database.get('testobject', self.test_object._id)
        self.assertIsNone(deleted_object)

    def tearDown(self):
        """
        Tear down the test case by closing the database connection.
        """
        self.test_database.close_connection()


if __name__ == '__main__':
    unittest.main()

