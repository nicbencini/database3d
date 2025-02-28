"""
A context file for the file path to the modules used in the tests
"""

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/src')

from database3d.database import model
