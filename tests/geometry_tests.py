"""
Tests for the geometry library.
"""

import unittest
import numpy as np

from context import vector3d # pylint: disable=import-error
from context import plane # pylint: disable=import-error


class VectorTests(unittest.TestCase):
    """
    Tests for the vector module.
    """

    def test_build_vector_instance(self):

        vec = vector3d.Vector3d([0,1,2])
        
        self.assertIsInstance(vec, vector3d.Vector3d)
        self.assertEqual(vec.x, 0)
        self.assertEqual(vec.y, 1)
        self.assertEqual(vec.z, 2)
    
    def test_modfiy_vector(self):

        vec = vector3d.Vector3d([0,0,0])

        vec.x = 0
        vec.y = 1
        vec.z = 2

        self.assertEqual(vec.x, 0)
        self.assertEqual(vec.y, 1)
        self.assertEqual(vec.z, 2)

    def test_incorrect_input_array(self):

        with self.assertRaises(ValueError):
            print(vector3d.Vector3d([0,0]))
        
        with self.assertRaises(ValueError):
            vector3d.Vector3d([0,0,0,0])

        with self.assertRaises(TypeError):
            vector3d.Vector3d(['a','b','c'])

        with self.assertRaises(TypeError):
            vector3d.Vector3d([True,True,True])

    def test_vector_equality(self):
        vec_1 = vector3d.Vector3d([11,23,2])
        vec_2 = vector3d.Vector3d([11,23,2])
        vec_3 = vector3d.Vector3d([1,2,2])

        self.assertTrue(vec_1 == vec_2)
        self.assertTrue(vec_1 == [11,23,2])
        self.assertFalse(vec_1 == vec_3)
        self.assertFalse(vec_1 == [1,1,1])
        
    
    def test_vector_magnitude(self):
        """Test for vector magnitude."""

        vector = vector3d.Vector3d([11,23,2])

        self.assertEqual(vector.magnitude(),25.573423705088842)
        self.assertEqual(vector3d.Vector3d.vector_magnitude(vector), 25.573423705088842)

    
    def test_vector_unit(self):
        """Test for unit vector."""

        vector = vector3d.Vector3d([11,23,2])

        unit_vector = vector.unit()
        control_vector = vector3d.Vector3d([0.4301340378531763,0.8993711700566414,0.07820618870057751])

        self.assertTrue(unit_vector == control_vector)

    @unittest.skip
    def test_vector_gram_schmit(self):
        """Test for gram schmit equation."""

        vector_1 = vector3d.Vector3d([11,23,2])
        vector_2 = vector3d.Vector3d([2,5,6])

        control_vector = vector3d.Vector3d([-1637,-3422,-292])

        self.assertTrue(vector3d.Vector3d.gram_schmit(vector_1 , vector_2) == control_vector)
    
    @unittest.skip
    def test_is_parallel(self):

        vector_1 = vector3d.Vector3d([0,0,1])
        vector_2 = vector3d.Vector3d([0,2,1])
        vector_3 = vector3d.Vector3d([0,0,1])

        self.assertFalse(vector_1.is_parallel_to(vector_2))
        self.assertTrue(vector_1.is_parallel_to(vector_3))

    @unittest.skip
    def test_local_plane(self):
        """Test for local plane."""

        point_1 = np.array([0.5,0.5,1])
        point_2 = np.array([1,0,0])
        vector = np.array([0,0,1])

        new_plane = plane.plane_from_3pt(point_1, point_2, vector)

        new_plane_origin = new_plane[0]
        new_plane_x_vec = new_plane[1]
        new_plane_y_vec = new_plane[2]
        new_plane_z_vec = new_plane[3]

        control_plane_origin = np.array([0.5, 0.5, 1])

        control_plane_x_vec = np.array([0.4082482904638631,
                                        -0.4082482904638631,
                                        -0.8164965809277261]
                                        )

        control_plane_y_vec = np.array([0.5773502691896258,
                                        -0.5773502691896258,
                                        0.5773502691896254]
                                        )

        control_plane_z_vec = np.array([-0.7071067811865476,
                                        -0.7071067811865476,
                                        0]
                                        )

        self.assertSequenceEqual(new_plane_origin.tolist(),control_plane_origin.tolist())
        self.assertSequenceEqual(new_plane_x_vec.tolist(),control_plane_x_vec.tolist())
        self.assertSequenceEqual(new_plane_y_vec.tolist(),control_plane_y_vec.tolist())
        self.assertSequenceEqual(new_plane_z_vec.tolist(),control_plane_z_vec.tolist())
    




if __name__ == '__main__':
    unittest.main()
