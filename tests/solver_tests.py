"""
Tests for the engine library.
"""

import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
import webbrowser

from context import model # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error

@unittest.skip
class LindSolverTests(unittest.TestCase):
    """
    Test for lind solver module.
    """

    def test_run_solver(self):
        """Test for building model database."""

        db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_4_truss_test.db'

        webbrowser.open('http://127.0.0.1:5000') # Launches solver online


if __name__ == '__main__':
    unittest.main()

