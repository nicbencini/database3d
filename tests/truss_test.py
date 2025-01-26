"""
Tests for the engine library.
"""

import os
import unittest
import numpy as np
import matplotlib.pyplot as plt

from context import database # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error
from context import element # pylint: disable=import-error

db_path_truss = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_4_truss_test.db'

class LindSolverTests(unittest.TestCase):
    """
    Test for 3 dimensional truss.
    """

    def test_build_pyramid(self):
        """Test for 3 dimensional truss."""

        structural_model = database.Model(db_path_truss)
        structural_model.build_tables()

        top_chord_list = []
        bottom_chord_list = []
        bracing_list = []

        section = properties.Section.default()
        orientation_vector = np.array([1,0,0])

        for i in range(9):

            node_1 = element.Node(i,0,0)
            node_2 = element.Node(i + 1,0,0)
            node_3 = element.Node(i,0,1)
            node_4 = element.Node(i + 1,0,1)

            bottom_chord = element.Bar(node_1,node_2,section,np.array([0,0,1]))
            top_chord = element.Bar(node_3,node_4,section,np.array([0,0,1]))
            bracing = element.Bar(node_1,node_4,section,np.array([0,0,1]))
            vertical = element.Bar(node_2,node_4,section,np.array([1,0,0]))

            top_chord_list.append(top_chord)
            bottom_chord_list.append(bottom_chord)
            bracing_list.append(bracing)
            bracing_list.append(vertical)

            if i == 0:
                vertical_2 = element.Bar(node_1,node_3,section,np.array([1,0,0]))
                bracing_list.append(vertical_2)

        support1 = element.Support.fix(bottom_chord_list[0].node_a)
        support2 = element.Support.fix(bottom_chord_list[-1].node_b)

        load1 = load.PointLoad(top_chord_list[5].node_a,0,0,-10,0,0,0)


        for bar in top_chord_list:
            structural_model.add_bar(bar)
        
        for bar in bottom_chord_list:
            structural_model.add_bar(bar)
        
        for bar in bracing_list:
            structural_model.add_bar(bar)

        structural_model.add_support(support1)
        structural_model.add_support(support2)

        structural_model.add_point_load(load1)

        #result = lind_solver.solve(structural_model)

        #structural_model.close_connection()        


if __name__ == '__main__':
    unittest.main()

