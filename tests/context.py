"""
A context file for the file path to the modules used in the tests
"""

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir + '/src')

from scpyce.database import model
from scpyce.objects import element
from scpyce.objects import properties
from scpyce.objects import load
from scpyce.geometry import vector_3d
from scpyce.geometry import plane
from scpyce.plot import plot
