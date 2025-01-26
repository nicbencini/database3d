"""
Tests for the geometry library.
"""

import unittest
import numpy as np

from context import vector_3d # pylint: disable=import-error
from context import plane # pylint: disable=import-error


class VectorTests(unittest.TestCase):
    """
    Tests for the vector module.
    """

    def test_vector_magnitude(self):
        """Test for vector magnitude."""

        vector = (11,23,2)

        magnitude = vector_3d.magnitude(vector)

        self.assertEqual(magnitude,25.573423705088842)

    def test_vector_unit(self):
        """Test for unit vector."""

        vector = (11,23,2)

        unit_vector = vector_3d.unit(vector)
        control_vector = np.array([0.4301340378531763,0.8993711700566414,0.07820618870057751])

        self.assertSequenceEqual(unit_vector.tolist(),control_vector.tolist())

    def test_vector_length(self):
        """Test for vector length."""

        vector_1 = (0,0,0)
        vector_2 = (11,23,2)

        length = vector_3d.length(vector_1, vector_2)
        control_length = 25.573423705088842

        self.assertEqual(length, control_length)

    def test_vector_gram_schmit(self):
        """Test for gram schmit equation."""

        vector_1 = (11,23,2)
        vector_2 = (2,5,6)

        new_vector = vector_3d.gram_schmit(vector_1 , vector_2)
        control_vector = np.array([-1637,-3422,-292])

        self.assertSequenceEqual(new_vector.tolist(),control_vector.tolist())


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
    
    def test_is_parallel(self):

        vector_1 = np.array([0,0,1])
        vector_2 = np.array([0,2,1])
        vector_3 = np.array([0,0,1])

        self.assertFalse(vector_3d.is_parallel(vector_1, vector_2))
        self.assertTrue(vector_3d.is_parallel(vector_1, vector_3))



if __name__ == '__main__':
    unittest.main()
