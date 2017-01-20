import csv
import matplotlib.pyplot as plt
import numpy as np
from constants import *

# dpi of figure
DPI=1000
# number of previous values to calculate average
TREND_ACCURACY=150

iterations=[]
scores=[]
averages=[]

with open(FILE_DATA, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		iterations.append(float(row[0]))
		scores.append(float(row[1]))
		# calculating trend
		averages.append(np.mean(scores[-TREND_ACCURACY:]))

# plotting real values
plt.plot(iterations, scores, 'r.')
# plotting trend
plt.plot(iterations, averages, "b")

plt.savefig(FILE_IMAGE, dpi=DPI)
