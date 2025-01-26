import os

from context import database # pylint: disable=import-error
from context import lind_solver # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error
from context import plot # pylint: disable=import-error

db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_4_truss_test.db'

structural_model = database.Model(db_path)
model_plot = plot.Plot(structural_model)

model_plot.show_model()
model_plot.show_supports(show_text=True)
model_plot.show_loads(show_text=True)
model_plot.show_displacements(5000)
model_plot.plot()

structural_model.close_connection()        



