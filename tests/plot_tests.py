import os

from context import model # pylint: disable=import-error
from context import element # pylint: disable=import-error
from context import properties # pylint: disable=import-error
from context import load # pylint: disable=import-error
from context import plot # pylint: disable=import-error

db_path = os.path.dirname(os.path.realpath(__file__)) +'/test_files/'+ 'database_5_truss_test.db'

structural_model = model.Model(db_path, 'test_user')
model_plot = plot.Plot(structural_model)

model_plot.show_model()
model_plot.show_supports(show_text=True)
model_plot.show_loads(show_text=True)
#model_plot.show_displacements(50000)
model_plot.plot()

structural_model.close_connection()        



