import glob
import os
from plot_chart import plot_func
import shutil

for file in os.listdir('images/'):
    file_path = os.path.join('images/', file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

for file in glob.glob('data/data_*'):
    plot_func(file)


