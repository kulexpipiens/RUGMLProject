import os
from constants import *

data_exists = os.path.exists(FILE_DATA)
iterations_exists = os.path.exists(FILE_ITERATIONS)
qvalues_exists = os.path.exists(FILE_QVALUES)
if (data_exists or iterations_exists or qvalues_exists):
    os.remove(FILE_DATA)
    os.remove(FILE_ITERATIONS)
    os.remove(FILE_QVALUES)
