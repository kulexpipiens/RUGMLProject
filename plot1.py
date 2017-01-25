import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import glob

# dpi of figure
DPI=500
# number of previous values to calculate average
TREND_ACCURACY=150

colors = ["#000000", "#0000FF", "#A52A2A", "#7FFF00", "#DC143C", "#006400", "#FF8C00", "#FF1493", "#FFD700", "#808080"]

def add_to_plot(file_name, i, lr):
	iterations = []
	scores = []
	averages = []
	
	with open(file_name, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			iterations.append(float(row[0]))
			scores.append(float(row[1]))
			# calculating trend
			averages.append(np.mean(scores[-TREND_ACCURACY:]))
			#du 15 di 1.0 sz 5
			if len(iterations) == 20000:
				break;
	l = lr#'0.'+str(i+1)
	#if i == 9: l = '1.0'
	plt.plot(iterations, averages, colors[i%len(colors)], label=l, linewidth=2)
i=0
for file in glob.glob('data/data_*'):
	namea = file.split('_')
	change = namea[2] == '15' and namea[6] == '1.0' and namea[8].split('.')[0] == '5'
	if change:
		add_to_plot(file, i, namea[4])
		i+=1

plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=1.5)
plt.savefig("images2/plot1.png", dpi=DPI)
